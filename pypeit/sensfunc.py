

import os
import inspect
import numpy as np
import scipy
from IPython import embed

from pypeit import msgs
from pypeit import ginga
from pypeit import masterframe
from pypeit import specobjs
from pypeit.core import flux_calib
from pypeit.core import telluric
from pypeit.spectrographs.util import load_spectrograph
from astropy.io import fits
from astropy import table
from pypeit.core import coadd1d


# TODO Add the data model up here as a standard thing, which is an astropy table.
# data model needs a tag on whether its merged or not. For merged specobjs, you only apply sensfunc directly coefficients
# are then nonsense. homogenize data model to be the same for both algorithms.

#TODO Should this be a master frame? I think not.
#TODO Standard output location for sensfunc?
#TODO What if the user wants to coadd exposures first for say a multi-detector instrument where detector runs in the wavelength
# dimension, then compute a single sensfunc, rather than one for each detector? In that case this routine would need to run
# on co-added data written in a different format? That is easy enough to do, but we need to require that that file
# have certain meta data in its header.


# TODO How do we deal with cases of multiple-detectors where detector runs in the spectral direction? This code currently
# knows nothing about detectors. This is a tricky case. The options are:
# 1) Flux calibrate each detector separately, and then apply detector specific sensfuncs. This works for longslit, but
# but will fail for multislit, since different slits have different wavelength coverage.
# 2) Co-add the standard star spectra in counts, and compute one global sensfunc for the data. This would work well for
# multislit, but it will fail in cases where the detectors have different througphut, since there will be jumps in the
# co-added spectrum across detector boundaries, making the sensunc discontinouus.

# TODO Define sensfunc data model here.



class SensFunc(object):
    """
    Class to generate sensitivity function from a standard star spectrum.

    Args:
        spec1dfile (str):
            PypeIt spec1d file for the standard file.
        sensfile (str):
            File to write sensitivity function to.
        par (parset object):
            Parset containing parameters for sensitivity function computation.
        multi_spec_det (list):
            List of detectors for which to create a spliced sensitivity function.  If passed the sensitivity function
            code will merge together the sensitivity functions for the specified list of detectors. This option is
            required for instruments which have multiple detectors arranged in the spectral direction.
        debug:
            Run the sensitivity function codes in debug mode sending diagnostic information to the screen.
    """

    # Superclass factory method generates the subclass instance
    @classmethod
    def get_instance(cls, spec1dfile, sensfile, par, debug=False):
        return next(c for c in cls.__subclasses__() if c.__name__ == par['algorithm'])(spec1dfile, sensfile, par, debug=debug)

    def __init__(self, spec1dfile, sensfile, par=None, debug=False):
        self.spec1dfile = spec1dfile
        self.sensfile = sensfile
        self.par = par
        self.debug = debug

        # Are we splicing together multiple detectors?
        self.splice_multi_det = True if self.par['multi_spec_det'] is not None else False
        # Core attributes that will be output to file
        self.meta_table = None
        self.out_table = None

        # Read in the Standard star data
        sobjs_std = (specobjs.SpecObjs.from_fitsfile(self.spec1dfile)).get_std(multi_spec_det=self.par['multi_spec_det'])
        # Put spectrograph info into meta
        self.wave, self.counts, self.counts_ivar, self.counts_mask, self.meta_spec, header = sobjs_std.unpack_object(ret_flam=False)
        self.norderdet = self.wave.shape[1]
        # Set spectrograph
        self.spectrograph = load_spectrograph(self.meta_spec['PYP_SPEC'])

        # If the user provided RA and DEC use those instead of what is in meta
        star_ra = self.meta_spec['RA'] if self.par['star_ra'] is None else self.par['star_ra']
        star_dec = self.meta_spec['DEC'] if self.par['star_dec'] is None else self.par['star_dec']
        # Read in standard star dictionary
        self.std_dict = flux_calib.get_standard_spectrum(star_type=self.par['star_type'], star_mag=self.par['star_mag'],
                                                         ra=star_ra, dec=star_dec)

    @property
    def algorithm(self):
        return self.par['algorithm']


    def compute_sensfunc(self):
        """
        Dummy method overloaded by subclasses

        Returns:
            meta_table, out_table

        """
        pass
        return None, None

    def run(self):
        meta_table, out_table = self.compute_sensfunc()
        if self.splice_multi_det:
            self.meta_table, self.out_table = self.splice_sensfunc(meta_table, out_table)
        else:
            self.meta_table, self.out_table = meta_table, out_table
        return self.meta_table, self.out_table

    def save(self):

        # Write to outfile
        msgs.info('Writing sensitivity function results to file: {:}'.format(self.sensfile))
        hdu_meta = fits.table_to_hdu(self.meta_table)
        hdu_meta.name = 'METADATA'
        hdu_out = fits.table_to_hdu(self.out_table)
        hdu_out.name = 'OUT_TABLE'
        hdulist = fits.HDUList()
        hdulist.append(hdu_meta)
        hdulist.append(hdu_out)
        hdulist.writeto(self.sensfile, overwrite=True)

    def load(self, sensfile):
        # Write to outfile
        msgs.info('Reading object and telluric models from file: {:}'.format(sensfile))
        meta_table = table.Table.read(sensfile, hdu=1)
        out_table = table.Table.read(sensfile, hdu=2)

        return meta_table, out_table

    def splice_sensfunc(self, meta_table, out_table):

        # splice the sensitivity functions together, and add the splice as a key in the meta_table
        # (since we cannot pack the splice into the output table since it has a different shape). Otherwise just return the
        # input arguments unchanged
        msgs.info('Merging sensfunc for {:d} detectors {:}'.format(self.norderdet, self.par['multi_spec_det']))
        # TODO Can add some logic here to slightly extrapolate on both ends by say 10%
        wave_splice_min = out_table['WAVE_MIN'].min()
        wave_splice_max = out_table['WAVE_MAX'].max()
        wave_splice, _, _ = coadd1d.get_wave_grid(
            out_table['WAVE'].T, wave_method='linear',wave_grid_min=wave_splice_min, wave_grid_max=wave_splice_max,
            samp_fact=1.0)
        sensfunc_splice = np.zeros_like(wave_splice)
        for idet in range(self.norderdet):
            wave_min = out_table['WAVE_MIN'][idet]
            wave_max = out_table['WAVE_MAX'][idet]
            splice_wave_mask = (wave_splice >= wave_min) & (wave_splice <= wave_max)
            sensfunc_splice[splice_wave_mask] = scipy.interpolate.interp1d(
            out_table['WAVE'][idet], out_table['SENSFUNC'][idet], kind='cubic', bounds_error=False,
            fill_value=0.0)(wave_splice[splice_wave_mask])

        #sensfunc_splice_mask  = sensfunc_splice > 0.0
        # Add the spliced information to the meta_table, since the size of the outpt table is fixed
        meta_table['SPLICE_MULTI_DET'] = True
        meta_table['WAVE_SPLICE'] = [wave_splice]
        meta_table['SENSFUNC_SPLICE'] = [sensfunc_splice]
        return meta_table, out_table


    def show(self):
        pass

# TODO Add a method which optionally merges sensfunc using the nsens > 1 logic



class IR(SensFunc):

    def __init__(self, spec1dfile, sensfile, par, debug=False):
        super().__init__(spec1dfile, sensfile, par, debug=debug)

        self.TelObj = None

    def compute_sensfunc(self):

        meta_table, out_table = telluric.sensfunc_telluric(
            self.wave, self.counts, self.counts_ivar, self.counts_mask, self.meta_spec['EXPTIME'],
            self.meta_spec['AIRMASS'], self.std_dict, self.par['IR']['telgridfile'], polyorder=self.par['polyorder'],
            sn_clip=self.par['IR']['sn_clip'], mask_abs_lines=self.par['mask_abs_lines'],
            # JFH Implement thease in parset?
            #delta_coeff_bounds=self.par['IR']['delta_coeff_bounds'],
            #minmax_coeff_bounds=self.par['IR']['min_max_coeff_bounds'],
            tol=self.par['IR']['tol'], popsize=self.par['IR']['popsize'], recombination=self.par['IR']['recombination'],
            polish=self.par['IR']['polish'],
            disp=self.par['IR']['disp'], debug=self.debug)
        # Add the algorithm to the meta_table
        meta_table['ALGORITHM'] = self.par['algorithm']

        return meta_table, out_table



class UVIS(SensFunc):
    def __init__(self, spec1dfile, sensfile, par, debug=False):
        super().__init__(spec1dfile, sensfile, par, debug=debug)

        # Add some cards to the meta spec. These should maybe just be added already in unpack object
        self.meta_spec['LATITUDE'] = self.spectrograph.telescope['latitude']
        self.meta_spec['LONGITUDE'] = self.spectrograph.telescope['longitude']


    def compute_sensfunc(self):

        meta_table, out_table = flux_calib.sensfunc(self.wave, self.counts, self.counts_ivar, self.counts_mask,
                                                              self.meta_spec['EXPTIME'], self.meta_spec['AIRMASS'], self.std_dict,
                                                              self.meta_spec['LONGITUDE'], self.meta_spec['LATITUDE'],
                                                              telluric=False, polyorder=self.par['polyorder'],
                                                              balm_mask_wid=self.par['UVIS']['balm_mask_wid'],
                                                              nresln=self.par['UVIS']['nresln'],
                                                              resolution=self.par['UVIS']['resolution'],
                                                              trans_thresh=self.par['UVIS']['trans_thresh'],
                                                              polycorrect=True, debug=self.debug)
        # Add the algorithm to the meta_table
        meta_table['ALGORITHM'] = self.par['algorithm']
        return meta_table, out_table

