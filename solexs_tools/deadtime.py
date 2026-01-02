#####################################################
# @Author: Abhilash Sarwade
# @Date:   2026-01-01 07:22:26 pm
# @email: sarwade@ursc.gov.in
# @File Name: deadtime.py
# @Project: solexs_tools
#
# @Last Modified time: 2026-01-02 03:43:00 pm
#####################################################

import os, argparse
import numpy as np
from astropy.io import fits
from .caldb_utils import get_caldb_base_dir

CALDB_BASE_DIR = get_caldb_base_dir()

def get_deadtime_params(SDD_number):

    dt_file = os.path.join(CALDB_BASE_DIR, "deadtime", f"solexs_deadtime_params_SDD{SDD_number}_v1.fits")
    
    with fits.open(dt_file) as hdul:
        
        # eff_factor = hdul[1].data['EFFICIENCY-FACTOR'][0]
        offset_cr1 = hdul[1].data['OFFSET-COUNTRATE-1'][0]
        offset_cr2 = hdul[1].data['OFFSET-COUNTRATE-2'][0]
        
    return offset_cr1, offset_cr2, dt_file

def apply_deadtime_correction(pi_file, hk_file, output_file=None,clobber=True):
    """
    Applies deadtime correction to a Type II PI file.
    Updates the EXPOSURE column based on HK data.
    """
    hdu1 = fits.open(pi_file)

    if hdu1[0].header['CONTENT'] != 'Type II PHA file':
        raise TypeError('Input File is not Type II PHA file.')


    if output_file is None:
        base, ext = os.path.splitext(pi_file)
        output_file = f"{base}_dt_corr{ext}"

    filter_sdd = hdu1[1].header['FILTER']
    offset_cr1, offset_cr2, dt_file = get_deadtime_params(filter_sdd)

    hk_hdul = fits.open(hk_file)
    hk_data = hk_hdul[1].data

    slow_cr = hk_data['SLOW_COUNTS']
    fast_cr = hk_data['FAST_COUNTS']
    
    if np.nanmin(fast_cr) < 500:
        offset_cr = offset_cr2
    else:
        offset_cr = offset_cr1

    corr_factor = (fast_cr - offset_cr) / slow_cr
    new_exposures = 1/corr_factor
    

    data = hdu1[1].data
    data['EXPOSURE'] = new_exposures

    header = hdu1[1].header

    header['HISTORY'] = f"Deadtime corrected using {os.path.basename(dt_file)}"
    header['HISTORY'] = f"Deadtime correction Offset Count Rate ={offset_cr}"

    if output_file is None:
        base, ext = os.path.splitext(pi_file)
        output_file = f"{base}_dt_corr{ext}"

    hdu1.writeto(output_file,overwrite=clobber)


def solexs_deadtime_correction_cli():
    parser = argparse.ArgumentParser(description="Apply Deadtime Correction to Level 1 PI spectrogram file (Type II)")

    parser.add_argument("-i", "--infile", required=True, help="Path to the Level 1 PI spectrogram file (Type II)")
    parser.add_argument("-hk", "--hkfile", required=True, help="Path to the Level 1 Housekeeping file")
    parser.add_argument("-o", "--outfile", help="Output filename (default: <input>_dt_corr.pi)")
    parser.add_argument('-c','--clobber', type=bool, default= False, help='Overwrite existing file if it exists')

    args = parser.parse_args()

    apply_deadtime_correction(args.infile, args.hkfile, args.outfile, args.clobber)