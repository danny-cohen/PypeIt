.. highlight:: rest

.. _configobj: http://configobj.readthedocs.io/en/latest/

.. _pypeitpar:

=================
PypeIt Parameters
=================

PypeIt allows you to customize its execution without having to change the
code directly.

Although not ubiquitous, most optional arguments of PypeIt's algorithms
are contained within the :class:`pypeit.par.pypeitpar.PypeItPar`
superset.  PypeIt uses the `configobj`_ class to parse the user-supplied
arguments  in the :ref:`pypeit_file` into an instance of
:class:`pypeit.par.pypeitpar.PypeItPar` that is passed to all of
PypeIt's main modules.  The syntax used to set parameters using the
:ref:`pypeit_file` is important and the nesting of the parameter changes
must match the `Current PypeItPar Parameter Hierarchy`_.

Importantly, each instrument served provides its own default values for
:class:`pypeit.par.pypeitpar.PypeItPar` as defined by its
``default_pypeit_par`` method; e.g.,
:func:`pypeit.spectrographs.shane_kast.ShaneKastSpectrograph.default_pypeit_par`.
Only those parameters that the user wishes to be different from the
default *as set by their specified instrument* need to be changed via
the :ref:`pypeit_file`.  The `Instrument-Specific Default
Configuration`_ are listed below.

.. warning::

 * Parsing of the PypeIt parameters from the :ref:`pypeit_file` does not
   yet check that the parameter group and keyword are valid.  This can
   make the syntax of the changes made incredibly important.  In
   particular, the indentation of the configuration lines, while useful
   for legibility, is irrelevant to how the lines are parsed.  For
   example, the following successfully changes the theshold for slit
   edge detection::
        
        [calibrations]
            [[slitedges]]
                edge_thresh = 100
    
   whereas the following fails silently::
        
        [calibrations]
            [slitedges]
                edge_thresh = 100

 - Default values of parameters that actually point to data files
   provided by PypeIt (e.g. the ``spectrum`` parameter for
   :class:`pypeit.par.pypeitpar.FlexurePar`) in its root directory will
   point to the relevant location on disk of whoever generated the
   documentation, which will be different for your installation.

How to change a parameter
=========================

To change a parameter, set its value at the beginning of your pypeit
file.  The *syntax* of the configuration block is important, but the
indentation is not.  The indentation will just make the block easier to
read.  All PypeIt files begin with the lines that set the spectrograph::

    [rdx]
        spectrograph = keck_deimos

The nesting of the PypeIt parameters is as illustrated in the `Current
PypeItPar Parameter Hierarchy`_ section below.  Here are a few examples
of how to change various parameters; for additional examples see the
`Instrument-Specific Default Configuration`_ section.

 * To change the threshold used for detecting slit/order edges, add::

    [calibrations]
        [[slitedges]]
            edge_thresh = 100

 * To change the exposure time range used to identify an arc and
   flat-field frames and to increase the LA Cosmic sigma-clipping
   threshold for arc frames, add::

    [calibrations]
        [[arcframe]]
            exprng = None,10
            [[process]]
                sigclip = 6.
        [[pixelflatframe]]
            exprng = 11,30

How to change the image processing parameters for all frame types
=================================================================

To change the base-level image processing parameters that will be
applied to *all* frame types, you can use the ``baseprocess`` parameter
group.  This allows you to set these parameters once instead of having
to include lines in your PypeIt file for each frame type.  Any
frame-type-specific alterations can still be made and will overwrite the
base-level processing parameters.  For example, to change the
sigma-clipping level used by the LA Cosmic routine to default to 3.0 but
to use a value of 6.0 for arc frames, you can add the following to your
PypeIt file::

    [baseprocess]
        sigclip = 3.0
    [calibrations]
        [[arcframe]]
            [[[process]]]
                sigclip = 6.0


Current PypeItPar Parameter Hierarchy
+++++++++++++++++++++++++++++++++++++

`PypeItPar Keywords`_

    ``[rdx]``: `ReduxPar Keywords`_

    ``[calibrations]``: `CalibrationsPar Keywords`_

        ``[[biasframe]]``: `FrameGroupPar Keywords`_

            ``[[[process]]]``: `ProcessImagesPar Keywords`_

        ``[[darkframe]]``: `FrameGroupPar Keywords`_

            ``[[[process]]]``: `ProcessImagesPar Keywords`_

        ``[[arcframe]]``: `FrameGroupPar Keywords`_

            ``[[[process]]]``: `ProcessImagesPar Keywords`_

        ``[[tiltframe]]``: `FrameGroupPar Keywords`_

            ``[[[process]]]``: `ProcessImagesPar Keywords`_

        ``[[pixelflatframe]]``: `FrameGroupPar Keywords`_

            ``[[[process]]]``: `ProcessImagesPar Keywords`_

        ``[[pinholeframe]]``: `FrameGroupPar Keywords`_

            ``[[[process]]]``: `ProcessImagesPar Keywords`_

        ``[[traceframe]]``: `FrameGroupPar Keywords`_

            ``[[[process]]]``: `ProcessImagesPar Keywords`_

        ``[[standardframe]]``: `FrameGroupPar Keywords`_

            ``[[[process]]]``: `ProcessImagesPar Keywords`_

        ``[[flatfield]]``: `FlatFieldPar Keywords`_

        ``[[wavelengths]]``: `WavelengthSolutionPar Keywords`_

        ``[[slitedges]]``: `EdgeTracePar Keywords`_

        ``[[tilts]]``: `WaveTiltsPar Keywords`_

    ``[scienceframe]``: `FrameGroupPar Keywords`_

        ``[[process]]``: `ProcessImagesPar Keywords`_

    ``[scienceimage]``: `ReducePar Keywords`_

        ``[[findobj]]``: `FindObjPar Keywords`_

        ``[[skysub]]``: `SkySubPar Keywords`_

        ``[[extraction]]``: `ExtractionPar Keywords`_

    ``[flexure]``: `FlexurePar Keywords`_

    ``[fluxcalib]``: `FluxCalibrationPar Keywords`_

    ``[coadd2d]``: `Coadd2DPar Keywords`_


----

PypeItPar Keywords
------------------

Class Instantiation: :class:`pypeit.par.pypeitpar.PypeItPar`

================  ================================================  =======  ==============================  ======================================================================================================================================================================================================================================================================================
Key               Type                                              Options  Default                         Description                                                                                                                                                                                                                                                                           
================  ================================================  =======  ==============================  ======================================================================================================================================================================================================================================================================================
``rdx``           :class:`pypeit.par.pypeitpar.ReduxPar`            ..       `ReduxPar Keywords`_            PypIt reduction rules.                                                                                                                                                                                                                                                                
``calibrations``  :class:`pypeit.par.pypeitpar.CalibrationsPar`     ..       `CalibrationsPar Keywords`_     Parameters for the calibration algorithms                                                                                                                                                                                                                                             
``scienceframe``  :class:`pypeit.par.pypeitpar.FrameGroupPar`       ..       `FrameGroupPar Keywords`_       The frames and combination rules for the science observations                                                                                                                                                                                                                         
``scienceimage``  :class:`pypeit.par.pypeitpar.ReducePar`           ..       `ReducePar Keywords`_           Parameters determining sky-subtraction, object finding, and extraction                                                                                                                                                                                                                
``flexure``       :class:`pypeit.par.pypeitpar.FlexurePar`          ..       `FlexurePar Keywords`_          Parameters used by the flexure-correction procedure.  Flexure corrections are not performed by default.  To turn on, either set the parameters in the 'flexure' parameter group or set 'flexure = True' in the 'rdx' parameter group to use the default flexure-correction parameters.
``fluxcalib``     :class:`pypeit.par.pypeitpar.FluxCalibrationPar`  ..       `FluxCalibrationPar Keywords`_  Parameters used by the flux-calibration procedure.  Flux calibration is not performed by default.  To turn on, either set the parameters in the 'fluxcalib' parameter group or set 'fluxcalib = True' in the 'rdx' parameter group to use the default flux-calibration parameters.    
``coadd2d``       :class:`pypeit.par.pypeitpar.Coadd2DPar`          ..       `Coadd2DPar Keywords`_          Par set to control 2D coadds.  Only used in the after-burner script.                                                                                                                                                                                                                  
================  ================================================  =======  ==============================  ======================================================================================================================================================================================================================================================================================


----

ReduxPar Keywords
-----------------

Class Instantiation: :class:`pypeit.par.pypeitpar.ReduxPar`

======================  ==========  ====================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================  ============================================  =================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
Key                     Type        Options                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Default                                       Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
======================  ==========  ====================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================  ============================================  =================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
``spectrograph``        str         ``gemini_gnirs``, ``keck_deimos``, ``keck_lris_blue``, ``keck_lris_red``, ``keck_lris_red_longonly``, ``keck_nires``, ``keck_hires_red``, ``keck_hires_blue``, ``mmt_binospec``, ``keck_nirspec_low``, ``keck_mosfire``, ``shane_kast_blue``, ``shane_kast_red``, ``shane_kast_red_ret``, ``tng_dolores``, ``wht_isis_blue``, ``vlt_xshooter_uvb``, ``vlt_xshooter_vis``, ``magellan_fire``, ``magellan_mage``, ``vlt_xshooter_nir``, ``gemini_gmos_south_ham``, ``gemini_gmos_north_e2v``, ``gemini_gmos_north_ham``, ``lbt_mods1r``, ``lbt_mods1b``, ``lbt_mods2r``, ``lbt_mods2b``, ``vlt_fors2``  ..                                            Spectrograph that provided the data to be reduced.  Options are: gemini_gnirs, keck_deimos, keck_lris_blue, keck_lris_red, keck_lris_red_longonly, keck_nires, keck_hires_red, keck_hires_blue, mmt_binospec, keck_nirspec_low, keck_mosfire, shane_kast_blue, shane_kast_red, shane_kast_red_ret, tng_dolores, wht_isis_blue, vlt_xshooter_uvb, vlt_xshooter_vis, magellan_fire, magellan_mage, vlt_xshooter_nir, gemini_gmos_south_ham, gemini_gmos_north_e2v, gemini_gmos_north_ham, lbt_mods1r, lbt_mods1b, lbt_mods2r, lbt_mods2b, vlt_fors2
``detnum``              int, list   ..                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    ..                                            Restrict reduction to a list of detector indices                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
``sortroot``            str         ..                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    ..                                            A filename given to output the details of the sorted files.  If None, the default is the root name of the pypeit file.  If off, no output is produced.                                                                                                                                                                                                                                                                                                                                                                                           
``calwin``              int, float  ..                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    0                                             The window of time in hours to search for calibration frames for a science frame                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
``scidir``              str         ..                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    ``Science``                                   Directory relative to calling directory to write science files.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
``qadir``               str         ..                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    ``QA``                                        Directory relative to calling directory to write quality assessment files.                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
``redux_path``          str         ..                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    ``/Users/westfall/Work/packages/pypeit/doc``  Path to folder for performing reductions.  Default is the current working directory.                                                                                                                                                                                                                                                                                                                                                                                                                                                             
``ignore_bad_headers``  bool        ..                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    False                                         Ignore bad headers (NOT recommended unless you know it is safe).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
======================  ==========  ====================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================  ============================================  =================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================


----

CalibrationsPar Keywords
------------------------

Class Instantiation: :class:`pypeit.par.pypeitpar.CalibrationsPar`

==================  ===================================================  =======  =================================  =========================================================================================================================================================================================
Key                 Type                                                 Options  Default                            Description                                                                                                                                                                              
==================  ===================================================  =======  =================================  =========================================================================================================================================================================================
``caldir``          str                                                  ..       ``default``                        If provided, it must be the full path to calling directory to write master files.                                                                                                        
``setup``           str                                                  ..       ..                                 If masters='force', this is the setup name to be used: e.g., C_02_aa .  The detector number is ignored but the other information must match the Master Frames in the master frame folder.
``trim``            bool                                                 ..       True                               Trim the frame to isolate the data                                                                                                                                                       
``badpix``          bool                                                 ..       True                               Make a bad pixel mask? Bias frames must be provided.                                                                                                                                     
``biasframe``       :class:`pypeit.par.pypeitpar.FrameGroupPar`          ..       `FrameGroupPar Keywords`_          The frames and combination rules for the bias correction                                                                                                                                 
``darkframe``       :class:`pypeit.par.pypeitpar.FrameGroupPar`          ..       `FrameGroupPar Keywords`_          The frames and combination rules for the dark-current correction                                                                                                                         
``arcframe``        :class:`pypeit.par.pypeitpar.FrameGroupPar`          ..       `FrameGroupPar Keywords`_          The frames and combination rules for the wavelength calibration                                                                                                                          
``tiltframe``       :class:`pypeit.par.pypeitpar.FrameGroupPar`          ..       `FrameGroupPar Keywords`_          The frames and combination rules for the wavelength tilts                                                                                                                                
``pixelflatframe``  :class:`pypeit.par.pypeitpar.FrameGroupPar`          ..       `FrameGroupPar Keywords`_          The frames and combination rules for the field flattening                                                                                                                                
``pinholeframe``    :class:`pypeit.par.pypeitpar.FrameGroupPar`          ..       `FrameGroupPar Keywords`_          The frames and combination rules for the pinholes                                                                                                                                        
``traceframe``      :class:`pypeit.par.pypeitpar.FrameGroupPar`          ..       `FrameGroupPar Keywords`_          The frames and combination rules for images used for slit tracing                                                                                                                        
``standardframe``   :class:`pypeit.par.pypeitpar.FrameGroupPar`          ..       `FrameGroupPar Keywords`_          The frames and combination rules for the spectrophotometric standard observations                                                                                                        
``flatfield``       :class:`pypeit.par.pypeitpar.FlatFieldPar`           ..       `FlatFieldPar Keywords`_           Parameters used to set the flat-field procedure                                                                                                                                          
``wavelengths``     :class:`pypeit.par.pypeitpar.WavelengthSolutionPar`  ..       `WavelengthSolutionPar Keywords`_  Parameters used to derive the wavelength solution                                                                                                                                        
``slitedges``       :class:`pypeit.par.pypeitpar.EdgeTracePar`           ..       `EdgeTracePar Keywords`_           Slit-edge tracing parameters                                                                                                                                                             
``tilts``           :class:`pypeit.par.pypeitpar.WaveTiltsPar`           ..       `WaveTiltsPar Keywords`_           Define how to trace the slit tilts using the trace frames                                                                                                                                
==================  ===================================================  =======  =================================  =========================================================================================================================================================================================


----

FlatFieldPar Keywords
---------------------

Class Instantiation: :class:`pypeit.par.pypeitpar.FlatFieldPar`

=======================  ==========  =====================  =============  =================================================================================================================================================================================================================================================
Key                      Type        Options                Default        Description                                                                                                                                                                                                                                      
=======================  ==========  =====================  =============  =================================================================================================================================================================================================================================================
``method``               str         ``bspline``, ``skip``  ``bspline``    Method used to flat field the data; use skip to skip flat-fielding.  Options are: None, bspline, skip                                                                                                                                            
``frame``                str         ..                     ``pixelflat``  Frame to use for field flattening.  Options are: "pixelflat", or a specified calibration filename.                                                                                                                                               
``illumflatten``         bool        ..                     True           Use the flat field to determine the illumination profile of each slit.                                                                                                                                                                           
``spec_samp_fine``       int, float  ..                     1.2            bspline break point spacing in units of pixels for spectral fit to flat field blaze function.                                                                                                                                                    
``spec_samp_coarse``     int, float  ..                     50.0           bspline break point spacing in units of pixels for 2-d bspline-polynomial fit to flat field image residuals. This should be a large number unless you are trying to fit a sky flat with lots of narrow spectral features.                        
``spat_samp``            int, float  ..                     5.0            Spatial sampling for slit illumination function. This is the width of the median filter in pixels used to determine the slit illumination function, and thus sets the minimum scale on which the illumination function will have features.       
``tweak_slits``          bool        ..                     True           Use the illumination flat field to tweak the slit edges. This will work even if illumflatten is set to False                                                                                                                                     
``tweak_slits_thresh``   float       ..                     0.93           If tweak_slits is True, this sets the illumination function threshold used to tweak the slit boundaries based on the illumination flat. It should be a number less than 1.0                                                                      
``tweak_slits_maxfrac``  float       ..                     0.1            If tweak_slit is True, this sets the maximum fractional amount (of a slits width) allowed for trimming each (i.e. left and right) slit boundary, i.e. the default is 10% which means slits would shrink or grow by at most 20% (10% on each side)
=======================  ==========  =====================  =============  =================================================================================================================================================================================================================================================


----

WavelengthSolutionPar Keywords
------------------------------

Class Instantiation: :class:`pypeit.par.pypeitpar.WavelengthSolutionPar`

====================  =========================  ======================================================================================================  ================  ==============================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
Key                   Type                       Options                                                                                                 Default           Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
====================  =========================  ======================================================================================================  ================  ==============================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
``reference``         str                        ``arc``, ``sky``, ``pixel``                                                                             ``arc``           Perform wavelength calibration with an arc, sky frame.  Use 'pixel' for no wavelength solution.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
``method``            str                        ``simple``, ``semi-brute``, ``basic``, ``holy-grail``, ``identify``, ``reidentify``, ``full_template``  ``holy-grail``    Method to use to fit the individual arc lines. Most of these methods are now deprecated as they fail most of the time without significant parameter tweaking. 'holy-grail' attempts to get a first guess at line IDs by looking for patterns in the line locations. It is fully automated and works really well excpet for when it does not'reidentify' is now the preferred method, however it requires that an archive of wavelength solution has been constructed for your instrument/grating combination                           Options are: simple, semi-brute, basic, holy-grail, identify, reidentify, full_template
``echelle``           bool                       ..                                                                                                      False             Is this an echelle spectrograph? If yes an additional 2-d fit wavelength fit will be performed as a function of spectral pixel and order number to improve the wavelength solution                                                                                                                                                                                                                                                                                                                                                                                                                                            
``ech_fix_format``    bool                       ..                                                                                                      True              Is this a fixed format echelle like ESI, X-SHOOTER, or NIRES. If so reidentification will assume that each order in the data is aligned with a single order in the reid arxiv                                                                                                                                                                                                                                                                                                                                                                                                                                                 
``ech_nspec_coeff``   int                        ..                                                                                                      4                 For echelle spectrographs, order of the final 2d fit to the spectral dimension. You should choose this to be the n_final of the fits to the individual orders.                                                                                                                                                                                                                                                                                                                                                                                                                                                                
``ech_norder_coeff``  int                        ..                                                                                                      4                 For echelle spectrographs, order of the final 2d fit to the order dimension.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
``ech_sigrej``        int, float                 ..                                                                                                      2.0               For echelle spectrographs sigma clipping rejection threshold in 2d fit to spectral and order dimensions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
``lamps``             list                       ..                                                                                                      ..                Name of one or more ions used for the wavelength calibration.  Use None for no calibration.  Options are: ArI, CdI, HgI, HeI, KrI, NeI, XeI, ZnI, ThAr                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
``nonlinear_counts``  float                      ..                                                                                                      10000000000.0     Arc lines above this saturation threshold are not used in wavelength solution fits because they cannotbe accurately centroided                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
``sigdetect``         int, float, list, ndarray  ..                                                                                                      5.0               Detection threshold for arc lines. This can be a single number or a list/array providing the value for each slit                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
``fwhm``              int, float                 ..                                                                                                      4.0               Spectral sampling of the arc lines. This is the FWHM of an arcline in *unbinned* pixels.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
``reid_arxiv``        str                        ..                                                                                                      ..                Name of the archival wavelength solution file that will be used for the wavelength reidentification if the wavelength solution method = reidentify                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
``nreid_min``         int                        ..                                                                                                      1                 Minimum number of times that a given candidate reidentified line must be properly matched with a line in the arxiv to be considered a good reidentification. If there is a lot of duplication in the arxiv of the spectra in question (i.e. multislit) set this to a number like 1-4. For echelle this depends on the number of solutions in the arxiv. For fixed format echelle (ESI, X-SHOOTER, NIRES) set this 1. For an echelle with a tiltable grating, it will depend on the number of solutions in the arxiv.                                                                                                          
``cc_thresh``         float, list, ndarray       ..                                                                                                      0.7               Threshold for the *global* cross-correlation coefficient between an input spectrum and member of the archive required to attempt reidentification. Spectra from the archive with a lower cross-correlation are not used for reidentification. This can be a single number or a list/array providing the value for each slit                                                                                                                                                                                                                                                                                                   
``cc_local_thresh``   float                      ..                                                                                                      0.7               Threshold for the *local* cross-correlation coefficient, evaluated at each reidentified line,  between an input spectrum and the shifted and stretched archive spectrum above which a line must be to be considered a good line for reidentification. The local cross-correlation is evaluated at each candidate reidentified line (using a window of nlocal_cc), and is then used to score the the reidentified lines to arrive at the final set of good reidentifications                                                                                                                                                   
``nlocal_cc``         int                        ..                                                                                                      11                Size of pixel window used for local cross-correlation computation for each arc line. If not an odd number one will be added to it to make it odd.                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
``rms_threshold``     float, list, ndarray       ..                                                                                                      0.15              Minimum RMS for keeping a slit/order solution. This can be a single number or a list/array providing the value for each slit                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
``match_toler``       float                      ..                                                                                                      2.0               Matching tolerance in pixels when searching for new lines. This is the difference in pixels between the wavlength assigned to an arc line by an iteration of the wavelength solution to the wavelength in the line list. This parameter is also used as the matching tolerance in pixels for a line reidentification. A good line match must match within this tolerance to the shifted and stretched archive spectrum, and the archive wavelength solution at this match must be within match_toler dispersion elements from the line in line list.                                                                          
``func``              str                        ..                                                                                                      ``legendre``      Function used for wavelength solution fits                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
``n_first``           int                        ..                                                                                                      2                 Order of first guess fit to the wavelength solution.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
``n_final``           int, float, list, ndarray  ..                                                                                                      4                 Order of final fit to the wavelength solution (there are n_final+1 parameters in the fit). This can be a single number or a list/array providing the value for each slit                                                                                                                                                                                                                                                                                                                                                                                                                                                      
``sigrej_first``      float                      ..                                                                                                      2.0               Number of sigma for rejection for the first guess to the wavelength solution.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
``sigrej_final``      float                      ..                                                                                                      3.0               Number of sigma for rejection for the final guess to the wavelength solution.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
``wv_cen``            float                      ..                                                                                                      0.0               Central wavelength. Backwards compatibility with basic and semi-brute algorithms.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
``disp``              float                      ..                                                                                                      0.0               Dispersion. Backwards compatibility with basic and semi-brute algorithms.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
``numsearch``         int                        ..                                                                                                      20                Number of brightest arc lines to search for in preliminary identification                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
``nfitpix``           int                        ..                                                                                                      5                 Number of pixels to fit when deriving the centroid of the arc lines (an odd number is best)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
``IDpixels``          int, float, list           ..                                                                                                      ..                One or more pixels at which to manually identify a line                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
``IDwaves``           int, float, list           ..                                                                                                      ..                Wavelengths of the manually identified lines                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
``medium``            str                        ``vacuum``, ``air``                                                                                     ``vacuum``        Medium used when wavelength calibrating the data.  Options are: vacuum, air                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
``frame``             str                        ``observed``, ``heliocentric``, ``barycentric``                                                         ``heliocentric``  Frame of reference for the wavelength calibration.  Options are: observed, heliocentric, barycentric                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
``nsnippet``          int                        ..                                                                                                      2                 Number of spectra to chop the arc spectrum into when using the full_template method                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
====================  =========================  ======================================================================================================  ================  ==============================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================


----

EdgeTracePar Keywords
---------------------

Class Instantiation: :class:`pypeit.par.pypeitpar.EdgeTracePar`

=======================  ================  ===========================================  ==============  ===========================================================================================================================================================================================================================================================================================================================================================================================================================================================================
Key                      Type              Options                                      Default         Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                
=======================  ================  ===========================================  ==============  ===========================================================================================================================================================================================================================================================================================================================================================================================================================================================================
``filt_iter``            int               ..                                           0               Number of median-filtering iterations to perform on sqrt(trace) image before applying to Sobel filter to detect slit/order edges.                                                                                                                                                                                                                                                                                                                                          
``sobel_mode``           str               ``nearest``, ``constant``                    ``nearest``     Mode for Sobel filtering.  Default is 'nearest'; note we find'constant' works best for DEIMOS.                                                                                                                                                                                                                                                                                                                                                                             
``edge_thresh``          int, float        ..                                           20.0            Threshold for finding edges in the Sobel-filtered significance image.                                                                                                                                                                                                                                                                                                                                                                                                      
``follow_span``          int               ..                                           20              In the initial connection of spectrally adjacent edge detections, this sets the number of previous spectral rows to consider when following slits forward.                                                                                                                                                                                                                                                                                                                 
``det_min_spec_length``  int, float        ..                                           0.33            The minimum spectral length (as a fraction of the detector size) of a trace determined by direct measurements of the detector data (as opposed to what should be included in any modeling approach; see fit_min_spec_length).                                                                                                                                                                                                                                              
``valid_flux_thresh``    int, float        ..                                           500.0           The flux in the image used to construct the edge traces is valid if its median value is above this threshold.  Any edge tracing issues are then assumed not to be an issue with the trace image itself.                                                                                                                                                                                                                                                                    
``max_shift_abs``        int, float        ..                                           0.5             Maximum spatial shift in pixels between an input edge location and the recentroided value.                                                                                                                                                                                                                                                                                                                                                                                 
``max_shift_adj``        int, float        ..                                           0.15            Maximum spatial shift in pixels between the edges in adjacent spectral positions.                                                                                                                                                                                                                                                                                                                                                                                          
``max_spat_error``       int, float        ..                                           ..              Maximum error in the spatial position of edges in pixels.                                                                                                                                                                                                                                                                                                                                                                                                                  
``match_tol``            int, float        ..                                           3.0             Same-side slit edges below this separation in pixels are considered part of the same edge.                                                                                                                                                                                                                                                                                                                                                                                 
``fit_function``         str               ``polynomial``, ``legendre``, ``chebyshev``  ``legendre``    Function fit to edge measurements.  Options are: polynomial, legendre, chebyshev                                                                                                                                                                                                                                                                                                                                                                                           
``fit_order``            int               ..                                           5               Order of the function fit to edge measurements.                                                                                                                                                                                                                                                                                                                                                                                                                            
``fit_maxdev``           int, float        ..                                           5.0             Maximum deviation between the fitted and measured edge position for rejection in spatial pixels.                                                                                                                                                                                                                                                                                                                                                                           
``fit_maxiter``          int               ..                                           25              Maximum number of rejection iterations during edge fitting.                                                                                                                                                                                                                                                                                                                                                                                                                
``fit_niter``            int               ..                                           1               Number of iterations of re-measuring and re-fitting the edge data; see :func:`pypeit.core.trace.fit_trace`.                                                                                                                                                                                                                                                                                                                                                                
``fit_min_spec_length``  float             ..                                           0.6             Minimum unmasked spectral length of a traced slit edge to use in any modeling procedure (polynomial fitting or PCA decomposition).                                                                                                                                                                                                                                                                                                                                         
``left_right_pca``       bool              ..                                           False           Construct a PCA decomposition for the left and right traces separately.  This can be important for cross-dispersed echelle spectrographs (e.g., Keck-NIRES)                                                                                                                                                                                                                                                                                                                
``pca_n``                int               ..                                           ..              The number of PCA components to keep, which must be less than the number of detected traces.  If not provided, determined by calculating the minimum number of components required to explain a given percentage of variance in the edge data; see `pca_var_percent`.                                                                                                                                                                                                      
``pca_var_percent``      int, float        ..                                           99.8            The percentage (i.e., not the fraction) of the variance in the edge data accounted for by the PCA used to truncate the number of PCA coefficients to keep (see `pca_n`).  Ignored if `pca_n` is provided directly.                                                                                                                                                                                                                                                         
``pca_function``         str               ``polynomial``, ``legendre``, ``chebyshev``  ``polynomial``  Type of function fit to the PCA coefficients for each component.  Options are: polynomial, legendre, chebyshev                                                                                                                                                                                                                                                                                                                                                             
``pca_order``            int               ..                                           2               Order of the function fit to the PCA coefficients.                                                                                                                                                                                                                                                                                                                                                                                                                         
``pca_sigrej``           int, float, list  ..                                           2.0, 2.0        Sigma rejection threshold for fitting PCA components. Individual numbers are used for both lower and upper rejection. A list of two numbers sets these explicitly (e.g., [2., 3.]).                                                                                                                                                                                                                                                                                        
``pca_maxrej``           int               ..                                           1               Maximum number of PCA coefficients rejected during a given fit iteration.                                                                                                                                                                                                                                                                                                                                                                                                  
``pca_maxiter``          int               ..                                           25              Maximum number of rejection iterations when fitting the PCA coefficients.                                                                                                                                                                                                                                                                                                                                                                                                  
``smash_range``          list              ..                                           0.0, 1.0        Range of the slit in the spectral direction (in fractional units) to smash when searching for slit edges.  If the spectrum covers only a portion of the image, use that range.                                                                                                                                                                                                                                                                                             
``edge_detect_clip``     int, float        ..                                           ..              Sigma clipping level for peaks detected in the collapsed, Sobel-filtered significance image.                                                                                                                                                                                                                                                                                                                                                                               
``trace_median_frac``    int, float        ..                                           ..              After detection of peaks in the rectified Sobel-filtered image and before refitting the edge traces, the rectified image is median filtered with a kernel width of `trace_median_frac*nspec` along the spectral dimension.                                                                                                                                                                                                                                                 
``trace_thresh``         int, float        ..                                           ..              After rectification and median filtering of the Sobel-filtered image (see `trace_median_frac`), values in the median-filtered image *below* this threshold are masked in the refitting of the edge trace data.  If None, no masking applied.                                                                                                                                                                                                                               
``fwhm_uniform``         int, float        ..                                           3.0             The `fwhm` parameter to use when using uniform weighting in :func:`pypeit.core.trace.fit_trace` when refining the PCA predictions of edges.  See description of :func:`pypeit.core.trace.peak_trace`.                                                                                                                                                                                                                                                                      
``niter_uniform``        int               ..                                           9               The number of iterations of :func:`pypeit.core.trace.fit_trace` to use when using uniform weighting.                                                                                                                                                                                                                                                                                                                                                                       
``fwhm_gaussian``        int, float        ..                                           3.0             The `fwhm` parameter to use when using Gaussian weighting in :func:`pypeit.core.trace.fit_trace` when refining the PCA predictions of edges.  See description :func:`pypeit.core.trace.peak_trace`.                                                                                                                                                                                                                                                                        
``niter_gaussian``       int               ..                                           6               The number of iterations of :func:`pypeit.core.trace.fit_trace` to use when using Gaussian weighting.                                                                                                                                                                                                                                                                                                                                                                      
``det_buffer``           int               ..                                           5               The minimum separation between the detector edges and a slit edge for any added edge traces.  Must be positive.                                                                                                                                                                                                                                                                                                                                                            
``max_nudge``            int               ..                                           ..              If parts of any (predicted) trace fall off the detector edge, allow them to be nudged away from the detector edge up to and including this maximum number of pixels.  If None, no limit is set; otherwise should be 0 or larger.                                                                                                                                                                                                                                           
``sync_predict``         str               ``pca``, ``nearest``                         ``pca``         Mode to use when predicting the form of the trace to insert.  Use `pca` to use the PCA decomposition or `nearest` to reproduce the shape of the nearest trace.                                                                                                                                                                                                                                                                                                             
``sync_center``          str               ``median``, ``nearest``, ``gap``             ``median``      Mode to use for determining the location of traces to insert.  Use `median` to use the median of the matched left and right edge pairs, `nearest` to use the length of the nearest slit, or `gap` to offset by a fixed gap width from the next slit edge.                                                                                                                                                                                                                  
``gap_offset``           int, float        ..                                           5.0             Offset (pixels) used for the slit edge gap width when inserting slit edges (see `sync_center`) or when nudging predicted slit edges to avoid slit overlaps.  This should be larger than `minimum_slit_gap` when converted to arcseconds.                                                                                                                                                                                                                                   
``sync_to_edge``         bool              ..                                           True            If adding a first left edge or a last right edge, ignore `center_mode` for these edges and place them at the edge of the detector (with the relevant shape).                                                                                                                                                                                                                                                                                                               
``minimum_slit_length``  int, float        ..                                           ..              Minimum slit length in arcsec.  Slit lengths are determined by the median difference between the left and right edge locations for the unmasked trace locations.  Short slits are masked or clipped.  If None, no minimum slit length applied.                                                                                                                                                                                                                             
``length_range``         int, float        ..                                           ..              Allowed range in slit length compared to the median slit length.  For example, a value of 0.3 means that slit lengths should not vary more than 30%.  Relatively shorter or longer slits are masked or clipped.  Most useful for echelle or multi-slit data where the slits should have similar or identical lengths.                                                                                                                                                      
``minimum_slit_gap``     int, float        ..                                           ..              Minimum slit gap in arcsec.  Gaps between slits are determined by the median difference between the right and left edge locations of adjacent slits.  Slits with small gaps are merged by removing the intervening traces.If None, no minimum slit gap is applied.  This should be smaller than `gap_offset` when converted to pixels.                                                                                                                                     
``clip``                 bool              ..                                           True            Instead of just masking bad slit trace edges, remove them.                                                                                                                                                                                                                                                                                                                                                                                                                 
``sync_clip``            bool              ..                                           True            For synchronized edges specifically, remove both edge traces, even if only one is selected for removal.                                                                                                                                                                                                                                                                                                                                                                    
``mask_reg_maxiter``     int               ..                                           ..              Maximum number of fit iterations to perform for registering slit-mask design and trace locations. If None, rejection iterations are performed until no points are rejected. If 1, only a single fit is performed without any rejection.                                                                                                                                                                                                                                    
``mask_reg_maxsep``      int, float        ..                                           ..              Maximum allowed separation between the calibrated coordinates of the designed slit position in pixels and the matched trace. If None, rejection is done iteratively using sigma clipping.  See mask_reg_sigrej.                                                                                                                                                                                                                                                            
``mask_reg_sigrej``      int, float        ..                                           5               Number of sigma for sigma-clipping during rejection iterations during the slit-mask design registration. If None, uses default set by `astropy.stats.sigma_clipped_stats`.                                                                                                                                                                                                                                                                                                 
``ignore_alignment``     bool              ..                                           False           Ignore any slit-mask designs identified as alignment slits.                                                                                                                                                                                                                                                                                                                                                                                                                
``pad``                  int               ..                                           0               Integer number of pixels to consider beyond the slit edges.                                                                                                                                                                                                                                                                                                                                                                                                                
``add_slits``            str, list         ..                                           ..              Add one or more user-defined slits.  The syntax to define a slit to add is: 'det:spec:spat_left:spat_right' where det=detector, spec=spectral pixel, spat_left=spatial pixel of left slit boundary, and spat_righ=spatial pixel of right slit boundary.  For example, '2:2000:2121:2322,3:2000:1201:1500' will add a slit to detector 2 passing through spec=2000 extending spatially from 2121 to 2322 and another on detector 3 at spec=2000 extending from 1201 to 1500.
``rm_slits``             str, list         ..                                           ..              Remove one or more user-specified slits.  The syntax used to define a slit to remove is: 'det:spec:spat' where det=detector, spec=spectral pixel, spat=spatial pixel.  For example, '2:2000:2121,3:2000:1500' will remove the slit on detector 2 that contains pixel (spat,spec)=(2000,2121) and on detector 3 that contains pixel (2000,2121).                                                                                                                            
=======================  ================  ===========================================  ==============  ===========================================================================================================================================================================================================================================================================================================================================================================================================================================================================


----

WaveTiltsPar Keywords
---------------------

Class Instantiation: :class:`pypeit.par.pypeitpar.WaveTiltsPar`

===================  =========================  =======  ==============  =========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
Key                  Type                       Options  Default         Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
===================  =========================  =======  ==============  =========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
``idsonly``          bool                       ..       False           Only use the arc lines that have an identified wavelength to trace tilts (CURRENTLY NOT USED!)                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
``tracethresh``      int, float, list, ndarray  ..       20.0            Significance threshold for arcs to be used in tracing wavelength tilts. This can be a single number or a list/array providing the value for each slit                                                                                                                                                                                                                                                                                                                                                                                                                    
``sig_neigh``        int, float                 ..       10.0            Significance threshold for arcs to be used in line identification for the purpose of identifying neighboring lines.The tracethresh parameter above determines the significance threshold of lines that will be traced, but these lines must be at least nfwhm_neigh fwhm away from neighboring lines. This parameter determines the significance above which a line must be to be considered a possible colliding neighbor. A low value of sig_neigh will result in an overall larger number of lines, which will result in more lines above tracethresh getting rejected
``nfwhm_neigh``      int, float                 ..       3.0             Required separation between neighboring arc lines for them to be considered for tilt tracing in units of the the spectral fwhm (see wavelength parset where fwhm is defined)                                                                                                                                                                                                                                                                                                                                                                                             
``maxdev_tracefit``  int, float                 ..       0.2             Maximum absolute deviation (in units of fwhm) for the legendre polynomial fits to individual arc line tilt fits during iterative trace fitting (flux weighted, then gaussian weighted)                                                                                                                                                                                                                                                                                                                                                                                   
``sigrej_trace``     int, float                 ..       3.0             Outlier rejection significance to determine which traced arc lines should be included in the global fit                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
``spat_order``       int, float, list, ndarray  ..       3               Order of the legendre polynomial to be fit to the the tilt of an arc line. This parameter determinesboth the orer of the *individual* arc line tilts, as well as the order of the spatial direction of the2d legendre polynomial (spatial, spectral) that is fit to obtain a global solution for the tilts across theslit/order. This can be a single number or a list/array providing the value for each slit                                                                                                                                                           
``spec_order``       int, float, list, ndarray  ..       4               Order of the spectral direction of the 2d legendre polynomial (spatial, spectral) that is fit to obtain a global solution for the tilts across the slit/order. This can be a single number or a list/array providing the value for each slit                                                                                                                                                                                                                                                                                                                             
``func2d``           str                        ..       ``legendre2d``  Type of function for 2D fit                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
``maxdev2d``         int, float                 ..       0.25            Maximum absolute deviation (in units of fwhm) rejection threshold used to determines which pixels in global 2d fits to arc line tilts are rejected because they deviate from the model by more than this value                                                                                                                                                                                                                                                                                                                                                           
``sigrej2d``         int, float                 ..       3.0             Outlier rejection significance determining which pixels on a fit to an arc line tilt are rejected by the global 2D fit                                                                                                                                                                                                                                                                                                                                                                                                                                                   
``rm_continuum``     bool                       ..       False           Before tracing the line center at each spatial position, remove any low-order continuum in the 2D spectra.                                                                                                                                                                                                                                                                                                                                                                                                                                                               
``cont_rej``         int, float, list, ndarray  ..       3, 1.5          The sigma threshold for rejection.  Can be a single number or two numbers that give the low and high sigma rejection, respectively.                                                                                                                                                                                                                                                                                                                                                                                                                                      
===================  =========================  =======  ==============  =========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================


----

FrameGroupPar Keywords
----------------------

Class Instantiation: :class:`pypeit.par.pypeitpar.FrameGroupPar`

=============  ==============================================  =======================================================================================================  ============================  ===============================================================================================================================================================================================================================================================
Key            Type                                            Options                                                                                                  Default                       Description                                                                                                                                                                                                                                                    
=============  ==============================================  =======================================================================================================  ============================  ===============================================================================================================================================================================================================================================================
``frametype``  str                                             ``tilt``, ``pixelflat``, ``science``, ``arc``, ``dark``, ``trace``, ``bias``, ``pinhole``, ``standard``  ``science``                   Frame type.  Options are: tilt, pixelflat, science, arc, dark, trace, bias, pinhole, standard                                                                                                                                                                  
``useframe``   str                                             ..                                                                                                       ``science``                   A master calibrations file to use if it exists.                                                                                                                                                                                                                
``number``     int                                             ..                                                                                                       0                             Used in matching calibration frames to science frames.  This sets the number of frames to use of this type                                                                                                                                                     
``exprng``     list                                            ..                                                                                                       None, None                    Used in identifying frames of this type.  This sets the minimum and maximum allowed exposure times.  There must be two items in the list.  Use None to indicate no limit; i.e., to select exposures with any time greater than 30 sec, use exprng = [30, None].
``process``    :class:`pypeit.par.pypeitpar.ProcessImagesPar`  ..                                                                                                       `ProcessImagesPar Keywords`_  Parameters used for basic image processing                                                                                                                                                                                                                     
=============  ==============================================  =======================================================================================================  ============================  ===============================================================================================================================================================================================================================================================


----

ProcessImagesPar Keywords
-------------------------

Class Instantiation: :class:`pypeit.par.pypeitpar.ProcessImagesPar`

================  ==========  =====================================================================  ================  =========================================================================================================================================================================================================================================================================
Key               Type        Options                                                                Default           Description                                                                                                                                                                                                                                                              
================  ==========  =====================================================================  ================  =========================================================================================================================================================================================================================================================================
``overscan``      str         ``polynomial``, ``savgol``, ``median``, ``none``                       ``savgol``        Method used to fit the overscan.  Options are: polynomial, savgol, median, none                                                                                                                                                                                          
``overscan_par``  int, list   ..                                                                     5, 65             Parameters for the overscan subtraction.  For 'polynomial', set overcan_par = order, number of pixels, number of repeats ; for 'savgol', set overscan_par = order, window size ; for 'median', set overscan_par = None or omit the keyword.                              
``match``         int, float  ..                                                                     -1                (Deprecate?) Match frames with pixel counts that are within N-sigma of one another, where match=N below.  If N < 0, nothing is matched.                                                                                                                                  
``combine``       str         ``mean``, ``median``, ``weightmean``                                   ``weightmean``    Method used to combine frames.  Options are: mean, median, weightmean                                                                                                                                                                                                    
``satpix``        str         ``reject``, ``force``, ``nothing``                                     ``reject``        Handling of saturated pixels.  Options are: reject, force, nothing                                                                                                                                                                                                       
``cr_reject``     bool        ..                                                                     False             Perform cosmic ray rejection                                                                                                                                                                                                                                             
``sigrej``        int, float  ..                                                                     20.0              Sigma level to reject cosmic rays (<= 0.0 means no CR removal)                                                                                                                                                                                                           
``n_lohi``        list        ..                                                                     0, 0              Number of pixels to reject at the lowest and highest ends of the distribution; i.e., n_lohi = low, high.  Use None for no limit.                                                                                                                                         
``sig_lohi``      list        ..                                                                     3.0, 3.0          Sigma-clipping level at the low and high ends of the distribution; i.e., sig_lohi = low, high.  Use None for no limit.                                                                                                                                                   
``replace``       str         ``min``, ``max``, ``mean``, ``median``, ``weightmean``, ``maxnonsat``  ``maxnonsat``     If all pixels are rejected, replace them using this method.  Options are: min, max, mean, median, weightmean, maxnonsat                                                                                                                                                  
``lamaxiter``     int         ..                                                                     1                 Maximum number of iterations for LA cosmics routine.                                                                                                                                                                                                                     
``grow``          int, float  ..                                                                     1.5               Factor by which to expand regions with cosmic rays detected by the LA cosmics routine.                                                                                                                                                                                   
``rmcompact``     bool        ..                                                                     True              Remove compact detections in LA cosmics routine                                                                                                                                                                                                                          
``sigclip``       int, float  ..                                                                     4.5               Sigma level for rejection in LA cosmics routine                                                                                                                                                                                                                          
``sigfrac``       int, float  ..                                                                     0.3               Fraction for the lower clipping threshold in LA cosmics routine.                                                                                                                                                                                                         
``objlim``        int, float  ..                                                                     3.0               Object detection limit in LA cosmics routine                                                                                                                                                                                                                             
``bias``          str         ``as_available``, ``force``, ``skip``                                  ``as_available``  Parameter for bias subtraction. Options are: (1) 'as_available' -- Bias subtract if bias frames were provided;  (2) 'force' -- Require bias subtraction; exception raised if no biases available;  (3) 'skip' -- Skip bias subtraction even if bias frames were provided.
================  ==========  =====================================================================  ================  =========================================================================================================================================================================================================================================================================


----

ReducePar Keywords
------------------

Class Instantiation: :class:`pypeit.par.pypeitpar.ReducePar`

==============  ===========================================  =======  =========================  =====================================================
Key             Type                                         Options  Default                    Description                                          
==============  ===========================================  =======  =========================  =====================================================
``findobj``     :class:`pypeit.par.pypeitpar.FindObjPar`     ..       `FindObjPar Keywords`_     Parameters for the find object and tracing algorithms
``skysub``      :class:`pypeit.par.pypeitpar.SkySubPar`      ..       `SkySubPar Keywords`_      Parameters for sky subtraction algorithms            
``extraction``  :class:`pypeit.par.pypeitpar.ExtractionPar`  ..       `ExtractionPar Keywords`_  Parameters for extraction algorithms                 
==============  ===========================================  =======  =========================  =====================================================


----

FindObjPar Keywords
-------------------

Class Instantiation: :class:`pypeit.par.pypeitpar.FindObjPar`

===========================  ==========  =======  =======  ===================================================================================================================================================================================================================
Key                          Type        Options  Default  Description                                                                                                                                                                                                        
===========================  ==========  =======  =======  ===================================================================================================================================================================================================================
``trace_npoly``              int         ..       5        Order of legendre polynomial fits to object traces.                                                                                                                                                                
``sig_thresh``               int, float  ..       10.0     Significance threshold for object finding.                                                                                                                                                                         
``find_trim_edge``           list        ..       5, 5     Trim the slit by this number of pixels left/right before finding objects                                                                                                                                           
``find_cont_fit``            bool        ..       True     Fit a continuum to the illumination pattern across the trace rectified image (masking objects) when searching for peaks to initially identify objects                                                              
``find_npoly_cont``          int         ..       1        Polynomial order for fitting continuum to the illumination pattern across the trace rectified image (masking objects) when searching for peaks to initially identify objects                                       
``find_maxdev``              int, float  ..       2.0      Maximum deviation of pixels from polynomial fit to trace used to reject bad pixels in trace fitting.                                                                                                               
``find_extrap_npoly``        int         ..       3        Polynomial order used for trace extrapolation                                                                                                                                                                      
``maxnumber``                int         ..       10       Maximum number of objects to extract in a science frame.  Use None for no limit.                                                                                                                                   
``find_fwhm``                int, float  ..       5.0      Indicates roughly the fwhm of objects in pixels for object finding                                                                                                                                                 
``ech_find_max_snr``         int, float  ..       1.0      Criteria for keeping echelle objects. They must either have a maximum S/N across all the orders greater than this value or satisfy the min_snr criteria described by the min_snr parameters                        
``ech_find_min_snr``         int, float  ..       0.3      Criteria for keeping echelle objects. They must either have a maximum S/N across all the orders greater than ech_find_max_snr,  value or they must have S/N > ech_find_min_snr on >= ech_find_nabove_min_snr orders
``ech_find_nabove_min_snr``  int         ..       2        Criteria for keeping echelle objects. They must either have a maximum S/N across all the orders greater than ech_find_max_snr,  value or they must have S/N > ech_find_min_snr on >= ech_find_nabove_min_snr orders
``skip_second_find``         bool        ..       False    Only perform one round of object finding (mainly for quick_look)                                                                                                                                                   
===========================  ==========  =======  =======  ===================================================================================================================================================================================================================


----

SkySubPar Keywords
------------------

Class Instantiation: :class:`pypeit.par.pypeitpar.SkySubPar`

===================  ==========  =======  =======  ========================================================================================================================================================================================================================================================================================================================================
Key                  Type        Options  Default  Description                                                                                                                                                                                                                                                                                                                             
===================  ==========  =======  =======  ========================================================================================================================================================================================================================================================================================================================================
``bspline_spacing``  int, float  ..       0.6      Break-point spacing for the bspline sky subtraction fits.                                                                                                                                                                                                                                                                               
``sky_sigrej``       float       ..       3.0      Rejection parameter for local sky subtraction                                                                                                                                                                                                                                                                                           
``global_sky_std``   bool        ..       True     Global sky subtraction will be performed on standard stars. This should be turnedoff for example for near-IR reductions with narrow slits, since bright standards canfill the slit causing global sky-subtraction to fail. In these situations we go straight to local sky-subtraction since it is designed to deal with such situations
``no_poly``          bool        ..       False    Turn off polynomial basis (Legendre) in global sky subtraction                                                                                                                                                                                                                                                                          
===================  ==========  =======  =======  ========================================================================================================================================================================================================================================================================================================================================


----

ExtractionPar Keywords
----------------------

Class Instantiation: :class:`pypeit.par.pypeitpar.ExtractionPar`

===================  ==========  =======  =======  =============================================================================================================================================================================================================================================================================================
Key                  Type        Options  Default  Description                                                                                                                                                                                                                                                                                  
===================  ==========  =======  =======  =============================================================================================================================================================================================================================================================================================
``boxcar_radius``    int, float  ..       1.5      Boxcar radius in arcseconds used for boxcar extraction                                                                                                                                                                                                                                       
``std_prof_nsigma``  float       ..       30.0     prof_nsigma parameter for Standard star extraction.  Prevents undesired rejection.                                                                                                                                                                                                           
``sn_gauss``         int, float  ..       4.0      S/N threshold for performing the more sophisticated optimal extraction which performs a b-spline fit to the object profile. For S/N < sn_gauss the code will simply optimal extractwith a Gaussian with FWHM determined from the object finding.                                             
``model_full_slit``  bool        ..       False    If True local sky subtraction will be performed on the entire slit. If False, local sky subtraction will be applied to only a restricted region around each object. This should be set to True for either multislit observations using narrow slits or echelle observations with narrow slits
``manual``           list        ..       ..       List of manual extraction parameter sets                                                                                                                                                                                                                                                     
``skip_optimal``     bool        ..       False    Perform boxcar extraction only (i.e. skip Optimal and local skysub)                                                                                                                                                                                                                          
===================  ==========  =======  =======  =============================================================================================================================================================================================================================================================================================


----

FlexurePar Keywords
-------------------

Class Instantiation: :class:`pypeit.par.pypeitpar.FlexurePar`

============  ==========  =================================  ==============================================================================  ======================================================================================================================================================================================================================
Key           Type        Options                            Default                                                                         Description                                                                                                                                                                                                           
============  ==========  =================================  ==============================================================================  ======================================================================================================================================================================================================================
``method``    str         ``boxcar``, ``slitcen``, ``skip``  ``skip``                                                                        Method used to correct for flexure. Use skip for no correction.  If slitcen is used, the flexure correction is performed before the extraction of objects (not recommended).  Options are: None, boxcar, slitcen, skip
``maxshift``  int, float  ..                                 20                                                                              Maximum allowed flexure shift in pixels.                                                                                                                                                                              
``spectrum``  str         ..                                 ``/Users/westfall/Work/packages/pypeit/pypeit/data/sky_spec/paranal_sky.fits``  Archive sky spectrum to be used for the flexure correction.                                                                                                                                                           
============  ==========  =================================  ==============================================================================  ======================================================================================================================================================================================================================


----

FluxCalibrationPar Keywords
---------------------------

Class Instantiation: :class:`pypeit.par.pypeitpar.FluxCalibrationPar`

====================  ========  =======  =======  =========================================================================================================================================================================================================================================
Key                   Type      Options  Default  Description                                                                                                                                                                                                                              
====================  ========  =======  =======  =========================================================================================================================================================================================================================================
``balm_mask_wid``     float     ..       5.0      Mask width for Balmer lines in Angstroms.                                                                                                                                                                                                
``std_file``          str       ..       ..       Standard star file to generate sensfunc                                                                                                                                                                                                  
``std_obj_id``        str, int  ..       ..       Specifies object in spec1d file to use as standard. The brightest object found is used otherwise.                                                                                                                                        
``sensfunc``          str       ..       ..       FITS file that contains or will contain the sensitivity function.                                                                                                                                                                        
``extinct_correct``   bool      ..       True     If extinct_correct=True the code will use an atmospheric extinction model to extinction correct the data below 10000A. Note that this correction makes no sense if one is telluric correcting and this shold be set to False             
``telluric_correct``  bool      ..       False    If telluric_correct=True the code will grab the sens_dict['telluric'] tag from the sensfunc dictionary and apply it to the data.                                                                                                         
``star_type``         str       ..       ..       Spectral type of the standard star (for near-IR mainly)                                                                                                                                                                                  
``star_mag``          float     ..       ..       Magnitude of the standard star (for near-IR mainly)                                                                                                                                                                                      
``multi_det``         list      ..       ..       List of detector numbers to splice together for multi-detector instruments (e.g. DEIMOS) They are assumed to be in order of increasing wavelength And that there is *no* overlap in wavelength across detectors (might be ok if there is)
``telluric``          bool      ..       False    If telluric=True the code creates a synthetic standard star spectrum using the Kurucz models, the sens func is created setting nresln=1.5 it contains the correction for telluric lines.                                                 
``poly_norder``       int       ..       5        Polynomial order for sensfunc fitting                                                                                                                                                                                                    
``polycorrect``       bool      ..       True     Whether you want to correct the sensfunc with polynomial in the telluric and recombination line regions                                                                                                                                  
====================  ========  =======  =======  =========================================================================================================================================================================================================================================


----

Coadd2DPar Keywords
-------------------

Class Instantiation: :class:`pypeit.par.pypeitpar.Coadd2DPar`

===========  =========  =======  ========  ===========================================================================
Key          Type       Options  Default   Description                                                                
===========  =========  =======  ========  ===========================================================================
``offsets``  list       ..       ..        User-input list of offsets for the images being combined.                  
``weights``  str, list  ..       ``auto``  Mode for the weights used to coadd images.  See coadd2d.py for all options.
===========  =========  =======  ========  ===========================================================================



Instrument-Specific Default Configuration
+++++++++++++++++++++++++++++++++++++++++

The following provides the changes to the global default parameters
provided above for each instrument.  That is, if one were to include
these in the PypeIt file, you would be reproducing the effect of the
`default_pypeit_par` method specific to each derived
:class:`pypeit.spectrographs.spectrograph.Spectrograph` class.

KECK DEIMOS
-----------
Alterations to the default parameters are::

  [rdx]
      spectrograph = keck_deimos
  [calibrations]
      [[biasframe]]
          number = 5
          exprng = None, 2
      [[darkframe]]
          exprng = 999999, None
      [[arcframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          exprng = None, 30
          [[[process]]]
              combine = median
              satpix = nothing
              sig_lohi = 10.0, 10.0
      [[pinholeframe]]
          exprng = 999999, None
      [[traceframe]]
          number = 3
          exprng = None, 30
      [[standardframe]]
          number = 1
      [[wavelengths]]
          lamps = ArI, NeI, KrI, XeI
          nonlinear_counts = 62258.25
          match_toler = 2.5
          n_first = 3
      [[slitedges]]
          edge_thresh = 50.0
          fit_order = 3
          minimum_slit_length = 4.0
          minimum_slit_gap = 0.25
          sync_clip = False
  [scienceframe]
      exprng = 30, None
      [[process]]
          sigclip = 4.0
          objlim = 1.5
  [flexure]
      method = boxcar

KECK LRISb
----------
Alterations to the default parameters are::

  [rdx]
      spectrograph = keck_lris_blue
  [calibrations]
      [[biasframe]]
          number = 5
          exprng = None, 1
      [[darkframe]]
          exprng = 999999, None
      [[arcframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          exprng = None, 30
          [[[process]]]
              satpix = nothing
      [[pinholeframe]]
          exprng = 999999, None
      [[traceframe]]
          number = 3
          exprng = None, 30
      [[standardframe]]
          number = 1
      [[wavelengths]]
          method = full_template
          lamps = NeI, ArI, CdI, KrI, XeI, ZnI, HgI
          nonlinear_counts = 56360.1
          sigdetect = 10.0
          rms_threshold = 0.2
          match_toler = 2.5
          n_first = 3
      [[slitedges]]
          edge_thresh = 15.0
          det_min_spec_length = 0.1
          fit_order = 3
          fit_min_spec_length = 0.2
          sync_center = gap
          minimum_slit_length = 6
  [scienceframe]
      exprng = 29, None
  [flexure]
      method = boxcar

KECK LRISr
----------
Alterations to the default parameters are::

  [rdx]
      spectrograph = keck_lris_red
  [calibrations]
      [[biasframe]]
          number = 5
          exprng = None, 1
      [[darkframe]]
          exprng = 999999, None
      [[arcframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          exprng = None, 30
          [[[process]]]
              satpix = nothing
      [[pinholeframe]]
          exprng = 999999, None
      [[traceframe]]
          number = 3
          exprng = None, 30
      [[standardframe]]
          number = 1
      [[wavelengths]]
          lamps = NeI, ArI, CdI, KrI, XeI, ZnI, HgI
          nonlinear_counts = 49806.6
          sigdetect = 10.0
          rms_threshold = 0.2
      [[slitedges]]
          fit_order = 3
          sync_center = gap
          minimum_slit_length = 6
      [[tilts]]
          tracethresh = 25
          maxdev_tracefit = 1.0
          spat_order = 4
          spec_order = 7
          maxdev2d = 1.0
          sigrej2d = 5.0
  [scienceframe]
      exprng = 29, None
      [[process]]
          sigclip = 5.0
          objlim = 5.0
  [scienceimage]
      [[skysub]]
          bspline_spacing = 0.8
  [flexure]
      method = boxcar

KECK LRISr
----------
Alterations to the default parameters are::

  [rdx]
      spectrograph = keck_lris_red
  [calibrations]
      [[biasframe]]
          number = 5
          exprng = None, 1
      [[darkframe]]
          exprng = 999999, None
      [[arcframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          exprng = None, 30
          [[[process]]]
              satpix = nothing
      [[pinholeframe]]
          exprng = 999999, None
      [[traceframe]]
          number = 3
          exprng = None, 30
      [[standardframe]]
          number = 1
      [[wavelengths]]
          lamps = NeI, ArI, CdI, KrI, XeI, ZnI, HgI
          nonlinear_counts = 56360.1
          sigdetect = 10.0
          rms_threshold = 0.2
      [[slitedges]]
          fit_order = 3
          sync_center = gap
          minimum_slit_length = 6
      [[tilts]]
          tracethresh = 25
          maxdev_tracefit = 1.0
          spat_order = 4
          spec_order = 7
          maxdev2d = 1.0
          sigrej2d = 5.0
  [scienceframe]
      exprng = 29, None
      [[process]]
          sigclip = 5.0
          objlim = 5.0
  [scienceimage]
      [[skysub]]
          bspline_spacing = 0.8
  [flexure]
      method = boxcar

KECK NIRES
----------
Alterations to the default parameters are::

  [rdx]
      spectrograph = keck_nires
  [calibrations]
      [[biasframe]]
          useframe = none
          number = 5
      [[darkframe]]
          exprng = 20, None
      [[arcframe]]
          number = 1
          exprng = 20, None
          [[[process]]]
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          [[[process]]]
              satpix = nothing
      [[traceframe]]
          number = 3
      [[standardframe]]
          number = 1
          exprng = None, 20
      [[flatfield]]
          illumflatten = False
      [[wavelengths]]
          method = reidentify
          echelle = True
          ech_norder_coeff = 6
          ech_sigrej = 3.0
          lamps = OH_NIRES
          nonlinear_counts = 760000.0
          fwhm = 5.0
          reid_arxiv = keck_nires.fits
          rms_threshold = 0.2
          n_final = 3, 4, 4, 4, 4
      [[slitedges]]
          fit_min_spec_length = 0.4
          left_right_pca = True
          trace_thresh = 10.0
      [[tilts]]
          tracethresh = 10.0
  [scienceframe]
      exprng = 20, None
      [[process]]
          satpix = nothing
          sigclip = 20.0
  [scienceimage]
      [[skysub]]
          bspline_spacing = 0.8
      [[extraction]]
          boxcar_radius = 0.75

KECK NIRSPEC
------------
Alterations to the default parameters are::

  [rdx]
      spectrograph = keck_nirspec_low
  [calibrations]
      [[biasframe]]
          number = 5
          [[[process]]]
              overscan = none
      [[darkframe]]
          exprng = 20, None
          [[[process]]]
              overscan = none
      [[arcframe]]
          number = 1
          exprng = 20, None
          [[[process]]]
              overscan = none
              sigrej = -1
              bias = skip
      [[tiltframe]]
          number = 1
          [[[process]]]
              overscan = none
              sigrej = -1
              bias = skip
      [[pixelflatframe]]
          number = 5
          [[[process]]]
              overscan = none
              satpix = nothing
              bias = force
      [[pinholeframe]]
          [[[process]]]
              overscan = none
      [[traceframe]]
          number = 3
          [[[process]]]
              overscan = none
              bias = force
      [[standardframe]]
          number = 1
          exprng = None, 20
          [[[process]]]
              overscan = none
              bias = skip
      [[flatfield]]
          tweak_slits_thresh = 0.8
      [[wavelengths]]
          lamps = OH_NIRES
          nonlinear_counts = 100000.0
          fwhm = 5.0
          rms_threshold = 0.2
      [[slitedges]]
          edge_thresh = 200.0
          sync_predict = nearest
  [scienceframe]
      exprng = 20, None
      [[process]]
          overscan = none
          satpix = nothing
          sigclip = 20.0
          bias = skip
  [scienceimage]
      [[skysub]]
          bspline_spacing = 0.8

KECK MOSFIRE
------------
Alterations to the default parameters are::

  [rdx]
      spectrograph = keck_mosfire
  [calibrations]
      [[biasframe]]
          useframe = none
          number = 5
          [[[process]]]
              overscan = none
      [[darkframe]]
          exprng = 20, None
          [[[process]]]
              overscan = none
      [[arcframe]]
          number = 1
          exprng = 20, None
          [[[process]]]
              overscan = none
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              overscan = none
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          [[[process]]]
              overscan = none
              satpix = nothing
      [[pinholeframe]]
          [[[process]]]
              overscan = none
      [[traceframe]]
          number = 3
          [[[process]]]
              overscan = none
      [[standardframe]]
          number = 1
          exprng = None, 20
          [[[process]]]
              overscan = none
      [[flatfield]]
          illumflatten = False
      [[wavelengths]]
          lamps = OH_NIRES
          nonlinear_counts = 1000000000.0
          fwhm = 5.0
          rms_threshold = 0.2
      [[slitedges]]
          edge_thresh = 50.0
          sync_predict = nearest
  [scienceframe]
      exprng = 20, None
      [[process]]
          overscan = none
          satpix = nothing
          sigclip = 20.0
  [scienceimage]
      [[skysub]]
          bspline_spacing = 0.8

SHANE KASTb
-----------
Alterations to the default parameters are::

  [rdx]
      spectrograph = shane_kast_blue
  [calibrations]
      [[biasframe]]
          number = 5
          exprng = None, 1
      [[darkframe]]
          exprng = 999999, None
      [[arcframe]]
          number = 1
          exprng = None, 61
          [[[process]]]
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          exprng = 0, None
          [[[process]]]
              satpix = nothing
      [[pinholeframe]]
          exprng = 999999, None
      [[traceframe]]
          number = 3
          exprng = 0, None
      [[standardframe]]
          number = 1
          exprng = 1, 61
      [[wavelengths]]
          method = full_template
          lamps = CdI, HgI, HeI
          nonlinear_counts = 49806.6
          rms_threshold = 0.2
          match_toler = 2.5
          n_first = 3
      [[slitedges]]
          sync_predict = nearest
      [[tilts]]
          maxdev_tracefit = 0.02
          spec_order = 5
          maxdev2d = 0.02
  [scienceframe]
      exprng = 61, None
  [flexure]
      method = boxcar
      spectrum = /Users/westfall/Work/packages/pypeit/pypeit/data/sky_spec/sky_kastb_600.fits

SHANE KASTr
-----------
Alterations to the default parameters are::

  [rdx]
      spectrograph = shane_kast_red
  [calibrations]
      [[biasframe]]
          number = 5
          exprng = None, 1
      [[darkframe]]
          exprng = 999999, None
      [[arcframe]]
          number = 1
          exprng = None, 61
          [[[process]]]
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          exprng = 0, None
          [[[process]]]
              satpix = nothing
      [[pinholeframe]]
          exprng = 999999, None
      [[traceframe]]
          number = 3
          exprng = 0, None
      [[standardframe]]
          number = 1
          exprng = 1, 61
      [[wavelengths]]
          lamps = NeI, HgI, HeI, ArI
          nonlinear_counts = 49806.6
      [[slitedges]]
          sync_predict = nearest
  [scienceframe]
      exprng = 61, None
  [flexure]
      method = boxcar

SHANE KASTr
-----------
Alterations to the default parameters are::

  [rdx]
      spectrograph = shane_kast_red_ret
  [calibrations]
      [[biasframe]]
          number = 5
          exprng = None, 1
      [[darkframe]]
          exprng = 999999, None
      [[arcframe]]
          number = 1
          exprng = None, 61
          [[[process]]]
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[pixelflatframe]]
          number = 3
          exprng = 0, None
          [[[process]]]
              satpix = nothing
      [[pinholeframe]]
          exprng = 999999, None
      [[traceframe]]
          number = 3
          exprng = 0, None
      [[standardframe]]
          number = 1
          exprng = 1, 61
      [[wavelengths]]
          lamps = NeI, HgI, HeI, ArI
          nonlinear_counts = 91200.0
      [[slitedges]]
          sync_predict = nearest
  [scienceframe]
      exprng = 61, None
  [flexure]
      method = boxcar

TNG DOLORES
-----------
Alterations to the default parameters are::

  [calibrations]
      [[biasframe]]
          number = 5
          exprng = None, 0.1
      [[darkframe]]
          exprng = 999999, None
      [[arcframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          [[[process]]]
              satpix = nothing
      [[pinholeframe]]
          exprng = 999999, None
      [[traceframe]]
          number = 3
      [[standardframe]]
          number = 1
  [scienceframe]
      exprng = 1, None

WHT ISISb
---------
Alterations to the default parameters are::

  [rdx]
      spectrograph = wht_isis_blue
  [calibrations]
      [[biasframe]]
          number = 5
          exprng = None, 1
          [[[process]]]
              overscan = none
      [[darkframe]]
          exprng = 999999, None
          [[[process]]]
              overscan = none
      [[arcframe]]
          number = 1
          exprng = None, 120
          [[[process]]]
              overscan = none
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              overscan = none
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          [[[process]]]
              overscan = none
              combine = median
              satpix = nothing
              sig_lohi = 10.0, 10.0
      [[pinholeframe]]
          exprng = 999999, None
          [[[process]]]
              overscan = none
      [[traceframe]]
          number = 3
          [[[process]]]
              overscan = none
      [[standardframe]]
          number = 1
          exprng = None, 120
          [[[process]]]
              overscan = none
      [[wavelengths]]
          method = full_template
          lamps = NeI, ArI, ArII, CuI
          nonlinear_counts = 49806.6
          sigdetect = 10.0
          n_first = 3
          n_final = 5
          wv_cen = 4859.0
          disp = 0.2
      [[slitedges]]
          sync_predict = nearest
  [scienceframe]
      exprng = 90, None
      [[process]]
          overscan = none

VLT XShooter_UVB
----------------
Alterations to the default parameters are::

  [rdx]
      spectrograph = vlt_xshooter_uvb
  [calibrations]
      [[biasframe]]
          number = 5
      [[arcframe]]
          number = 1
          [[[process]]]
              overscan = median
              sigrej = -1
              bias = skip
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
              bias = skip
      [[pixelflatframe]]
          number = 5
          [[[process]]]
              satpix = nothing
      [[traceframe]]
          number = 3
          [[[process]]]
              overscan = median
      [[standardframe]]
          number = 1
      [[wavelengths]]
          method = reidentify
          echelle = True
          ech_norder_coeff = 5
          ech_sigrej = 3.0
          lamps = ThAr_XSHOOTER_UVB
          nonlinear_counts = 55900.0
          reid_arxiv = vlt_xshooter_uvb1x1_iraf.json
          rms_threshold = 0.5
      [[slitedges]]
          edge_thresh = 8.0
          max_shift_adj = 0.5
          left_right_pca = True
          trace_thresh = 10.0
          length_range = 0.3
  [scienceframe]
      useframe = overscan

VLT XShooter_VIS
----------------
Alterations to the default parameters are::

  [rdx]
      spectrograph = vlt_xshooter_vis
  [calibrations]
      [[biasframe]]
          number = 5
      [[arcframe]]
          number = 1
          [[[process]]]
              overscan = median
              sigrej = -1
              bias = skip
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
              bias = skip
      [[pixelflatframe]]
          number = 5
          [[[process]]]
              satpix = nothing
      [[traceframe]]
          number = 3
          [[[process]]]
              overscan = median
      [[standardframe]]
          number = 1
      [[flatfield]]
          tweak_slits_thresh = 0.9
      [[wavelengths]]
          method = reidentify
          echelle = True
          ech_sigrej = 3.0
          lamps = ThAr_XSHOOTER_VIS
          nonlinear_counts = 56360.1
          fwhm = 11.0
          reid_arxiv = vlt_xshooter_vis1x1.fits
          cc_thresh = 0.5
          cc_local_thresh = 0.5
          rms_threshold = 0.5
          n_final = 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3
      [[slitedges]]
          edge_thresh = 8.0
          max_shift_adj = 0.5
          fit_order = 8
          left_right_pca = True
          trace_thresh = 10.0
          length_range = 0.3
      [[tilts]]
          tracethresh = 15
          spec_order = 5
  [scienceframe]
      useframe = overscan
  [scienceimage]
      [[findobj]]
          find_trim_edge = 3, 3
          find_cont_fit = False
          find_npoly_cont = 0
      [[skysub]]
          bspline_spacing = 0.5
          global_sky_std = False
      [[extraction]]
          model_full_slit = True

VLT XShooter_NIR
----------------
Alterations to the default parameters are::

  [rdx]
      spectrograph = vlt_xshooter_nir
  [calibrations]
      [[biasframe]]
          number = 5
      [[arcframe]]
          number = 1
          [[[process]]]
              sigrej = -1
              bias = skip
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
              bias = skip
      [[pixelflatframe]]
          number = 5
          [[[process]]]
              satpix = nothing
              bias = force
      [[traceframe]]
          number = 3
          [[[process]]]
              bias = force
      [[standardframe]]
          number = 1
          [[[process]]]
              bias = skip
      [[flatfield]]
          illumflatten = False
          tweak_slits_thresh = 0.9
      [[wavelengths]]
          method = reidentify
          echelle = True
          ech_nspec_coeff = 5
          ech_norder_coeff = 5
          ech_sigrej = 3.0
          lamps = OH_XSHOOTER
          nonlinear_counts = 172000.0
          sigdetect = 10.0
          fwhm = 5.0
          reid_arxiv = vlt_xshooter_nir.fits
          cc_thresh = 0.5
          cc_local_thresh = 0.5
          rms_threshold = 0.25
      [[slitedges]]
          edge_thresh = 50.0
          max_shift_adj = 0.5
          fit_order = 8
          fit_min_spec_length = 0.5
          left_right_pca = True
          trace_thresh = 10.0
          length_range = 0.3
      [[tilts]]
          tracethresh = 25.0
          maxdev_tracefit = 0.04
          maxdev2d = 0.04
          rm_continuum = True
  [scienceframe]
      [[process]]
          satpix = nothing
          sigclip = 20.0
          bias = skip
  [scienceimage]
      [[findobj]]
          trace_npoly = 8
          find_cont_fit = False
          find_npoly_cont = 0
      [[skysub]]
          bspline_spacing = 0.8
          global_sky_std = False
      [[extraction]]
          model_full_slit = True

GEMINI-N GNIRS
--------------
Alterations to the default parameters are::

  [rdx]
      spectrograph = gemini_gnirs
  [calibrations]
      [[biasframe]]
          useframe = none
          [[[process]]]
              overscan = none
      [[darkframe]]
          [[[process]]]
              overscan = none
      [[arcframe]]
          number = 1
          [[[process]]]
              overscan = none
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              overscan = none
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          exprng = None, 30
          [[[process]]]
              overscan = none
              satpix = nothing
      [[pinholeframe]]
          [[[process]]]
              overscan = none
      [[traceframe]]
          number = 5
          exprng = None, 30
          [[[process]]]
              overscan = none
      [[standardframe]]
          number = 1
          exprng = None, 30
          [[[process]]]
              overscan = none
      [[flatfield]]
          illumflatten = False
          tweak_slits_thresh = 0.9
      [[wavelengths]]
          method = reidentify
          echelle = True
          ech_nspec_coeff = 3
          ech_norder_coeff = 5
          ech_sigrej = 3.0
          lamps = OH_GNIRS
          nonlinear_counts = 106500.0
          reid_arxiv = gemini_gnirs.fits
          cc_thresh = 0.6
          rms_threshold = 1.0
          n_final = 1, 3, 3, 3, 3, 3
      [[slitedges]]
          max_shift_adj = 0.5
          fit_min_spec_length = 0.5
          left_right_pca = True
          pca_order = 3
          trace_thresh = 10.0
      [[tilts]]
          tracethresh = 5.0, 10, 10, 10, 10, 10
          sig_neigh = 5.0
          nfwhm_neigh = 2.0
  [scienceframe]
      exprng = 30, None
  [scienceimage]
      [[findobj]]
          sig_thresh = 5.0
          find_trim_edge = 2, 2
          find_cont_fit = False
          find_npoly_cont = 0
      [[skysub]]
          bspline_spacing = 0.8
          global_sky_std = False
          no_poly = True
      [[extraction]]
          model_full_slit = True

GEMINI-S GMOS-S
---------------
Alterations to the default parameters are::

  [calibrations]
      [[biasframe]]
          number = 5
      [[arcframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          [[[process]]]
              combine = median
              satpix = nothing
              sig_lohi = 10.0, 10.0
      [[traceframe]]
          number = 3
      [[standardframe]]
          number = 1
      [[wavelengths]]
          method = full_template
          lamps = CuI, ArI, ArII
          rms_threshold = 0.4
          nsnippet = 1
      [[slitedges]]
          fit_order = 3
      [[tilts]]
          tracethresh = 10.0
  [flexure]
      method = boxcar

GEMINI-N GMOS-N
---------------
Alterations to the default parameters are::

  [calibrations]
      [[biasframe]]
          number = 5
      [[arcframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          [[[process]]]
              combine = median
              satpix = nothing
              sig_lohi = 10.0, 10.0
      [[traceframe]]
          number = 3
      [[standardframe]]
          number = 1
      [[wavelengths]]
          method = full_template
          lamps = CuI, ArI, ArII
          rms_threshold = 0.4
          nsnippet = 1
      [[slitedges]]
          fit_order = 3
      [[tilts]]
          tracethresh = 10.0
  [flexure]
      method = boxcar

GEMINI-N GMOS-N
---------------
Alterations to the default parameters are::

  [calibrations]
      [[biasframe]]
          number = 5
      [[arcframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          [[[process]]]
              combine = median
              satpix = nothing
              sig_lohi = 10.0, 10.0
      [[traceframe]]
          number = 3
      [[standardframe]]
          number = 1
      [[wavelengths]]
          method = full_template
          lamps = CuI, ArI, ArII
          rms_threshold = 0.4
          nsnippet = 1
      [[slitedges]]
          fit_order = 3
      [[tilts]]
          tracethresh = 10.0
  [flexure]
      method = boxcar

MAGELLAN FIRE
-------------
Alterations to the default parameters are::

  [rdx]
      spectrograph = magellan_fire
  [calibrations]
      [[biasframe]]
          useframe = overscan
      [[darkframe]]
          exprng = 20, None
      [[arcframe]]
          number = 1
          exprng = 20, None
          [[[process]]]
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          [[[process]]]
              satpix = nothing
      [[traceframe]]
          number = 5
      [[standardframe]]
          number = 1
          exprng = None, 60
      [[wavelengths]]
          echelle = True
          ech_sigrej = 3.0
          lamps = OH_XSHOOTER
          nonlinear_counts = 20000.0
          rms_threshold = 0.2
      [[slitedges]]
          edge_thresh = 50
          max_shift_adj = 0.5
          left_right_pca = True
      [[tilts]]
          tracethresh = 10, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 10
  [scienceframe]
      exprng = 20, None
      [[process]]
          satpix = nothing
          sigclip = 20.0

MAGELLAN MagE
-------------
Alterations to the default parameters are::

  [rdx]
      spectrograph = magellan_mage
  [calibrations]
      [[biasframe]]
          number = 5
      [[darkframe]]
          exprng = 20, None
      [[arcframe]]
          number = 1
          exprng = 20, None
          [[[process]]]
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          [[[process]]]
              satpix = nothing
      [[traceframe]]
          number = 3
      [[standardframe]]
          number = 1
          exprng = None, 20
      [[wavelengths]]
          method = reidentify
          echelle = True
          ech_sigrej = 3.0
          lamps = ThAr_MagE
          nonlinear_counts = 64879.65
          reid_arxiv = magellan_mage.fits
          cc_thresh = 0.5
          cc_local_thresh = 0.5
          rms_threshold = 0.2
      [[slitedges]]
          edge_thresh = 10.0
          max_shift_adj = 3.0
          fit_min_spec_length = 0.3
          left_right_pca = True
      [[tilts]]
          tracethresh = 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10
  [scienceframe]
      exprng = 20, None
      [[process]]
          satpix = nothing
          sigclip = 20.0
  [scienceimage]
      [[findobj]]
          find_trim_edge = 4, 4

KECK HIRES_R
------------
Alterations to the default parameters are::

  [rdx]
      spectrograph = keck_hires_red
  [calibrations]
      [[biasframe]]
          number = 5
      [[arcframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          [[[process]]]
              satpix = nothing
      [[traceframe]]
          number = 3
      [[standardframe]]
          number = 1
          exprng = None, 600
      [[wavelengths]]
          echelle = True
          ech_sigrej = 3.0
          lamps = ThAr
          nonlinear_counts = 56360.1
          rms_threshold = 0.25
      [[slitedges]]
          edge_thresh = 600.0
          max_shift_adj = 0.5
          left_right_pca = True
  [scienceframe]
      exprng = 600, None
      [[process]]
          satpix = nothing
          sigclip = 20.0

LBT MODS1R
----------
Alterations to the default parameters are::

  [rdx]
      spectrograph = lbt_mods1r
  [calibrations]
      [[biasframe]]
          number = 5
          exprng = None, 1
      [[darkframe]]
          exprng = 999999, None
      [[arcframe]]
          number = 1
          exprng = None, 60
          [[[process]]]
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          exprng = 0, None
          [[[process]]]
              satpix = nothing
      [[pinholeframe]]
          exprng = 999999, None
      [[traceframe]]
          number = 5
          exprng = 0, None
      [[standardframe]]
          number = 1
          exprng = 1, 200
      [[wavelengths]]
          lamps = OH_MODS
          nonlinear_counts = 64879.65
          fwhm = 10.0
          rms_threshold = 1.0
          n_first = 1
      [[slitedges]]
          edge_thresh = 300
      [[tilts]]
          maxdev_tracefit = 0.02
          spat_order = 5
          spec_order = 5
          maxdev2d = 0.02
  [scienceframe]
      exprng = 200, None

LBT MODS1B
----------
Alterations to the default parameters are::

  [rdx]
      spectrograph = lbt_mods1b
  [calibrations]
      [[biasframe]]
          number = 5
          exprng = None, 1
      [[darkframe]]
          exprng = 999999, None
      [[arcframe]]
          number = 1
          exprng = None, 60
          [[[process]]]
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          exprng = 0, None
          [[[process]]]
              satpix = nothing
      [[pinholeframe]]
          exprng = 999999, None
      [[traceframe]]
          number = 5
          exprng = 0, None
      [[standardframe]]
          number = 1
          exprng = 1, 200
      [[wavelengths]]
          lamps = XeI, ArII, ArI, NeI, KrI
          nonlinear_counts = 64879.65
          rms_threshold = 0.2
          n_first = 1
      [[slitedges]]
          edge_thresh = 300
      [[tilts]]
          maxdev_tracefit = 0.02
          spec_order = 5
          maxdev2d = 0.02
  [scienceframe]
      exprng = 200, None

LBT MODS2R
----------
Alterations to the default parameters are::

  [rdx]
      spectrograph = lbt_mods2r
  [calibrations]
      [[biasframe]]
          number = 5
          exprng = None, 1
      [[darkframe]]
          exprng = 999999, None
      [[arcframe]]
          number = 1
          exprng = None, 60
          [[[process]]]
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          exprng = 0, None
          [[[process]]]
              satpix = nothing
      [[pinholeframe]]
          exprng = 999999, None
      [[traceframe]]
          number = 5
          exprng = 0, None
      [[standardframe]]
          number = 1
          exprng = 1, 200
      [[wavelengths]]
          lamps = OH_MODS
          nonlinear_counts = 64879.65
          fwhm = 10.0
          rms_threshold = 1.0
          n_first = 1
      [[slitedges]]
          edge_thresh = 300
      [[tilts]]
          maxdev_tracefit = 0.02
          spec_order = 5
          maxdev2d = 0.02
  [scienceframe]
      exprng = 200, None

LBT MODS2B
----------
Alterations to the default parameters are::

  [rdx]
      spectrograph = lbt_mods2b
  [calibrations]
      [[biasframe]]
          number = 5
          exprng = None, 1
      [[darkframe]]
          exprng = 999999, None
      [[arcframe]]
          number = 1
          exprng = None, 60
          [[[process]]]
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          exprng = 0, None
          [[[process]]]
              satpix = nothing
      [[pinholeframe]]
          exprng = 999999, None
      [[traceframe]]
          number = 5
          exprng = 0, None
      [[standardframe]]
          number = 1
          exprng = 1, 200
      [[wavelengths]]
          lamps = XeI, ArII, ArI, NeI, KrI
          nonlinear_counts = 64879.65
          rms_threshold = 0.2
          n_first = 1
      [[slitedges]]
          edge_thresh = 300
      [[tilts]]
          maxdev_tracefit = 0.02
          spec_order = 5
          maxdev2d = 0.02
  [scienceframe]
      exprng = 200, None

VLT FORS2
---------
Alterations to the default parameters are::

  [rdx]
      spectrograph = vlt_fors2
  [calibrations]
      [[biasframe]]
          number = 5
          [[[process]]]
              overscan = median
      [[darkframe]]
          [[[process]]]
              overscan = median
      [[arcframe]]
          number = 1
          [[[process]]]
              overscan = median
              sigrej = -1
      [[tiltframe]]
          number = 1
          [[[process]]]
              overscan = median
              sigrej = -1
      [[pixelflatframe]]
          number = 5
          [[[process]]]
              overscan = median
              satpix = nothing
      [[pinholeframe]]
          [[[process]]]
              overscan = median
      [[traceframe]]
          number = 3
          [[[process]]]
              overscan = median
      [[standardframe]]
          number = 1
          [[[process]]]
              overscan = median
      [[flatfield]]
          illumflatten = False
          tweak_slits_thresh = 0.9
      [[wavelengths]]
          lamps = HeI, ArI
          sigdetect = 10.0
          rms_threshold = 0.25
      [[slitedges]]
          edge_thresh = 50.0
          max_shift_adj = 0.5
          fit_order = 3
      [[tilts]]
          tracethresh = 25.0
  [flexure]
      method = boxcar

