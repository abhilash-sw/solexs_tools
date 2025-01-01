#####################################################
# @Author: SoLEXSPOC
# @Date:   2024-12-31 02:19:09 pm
# @email: sarwade@ursc.gov.in
# @File Name: solexs_genlc.py
# @Project: solexs_tools
#
# @Last Modified time: 2025-01-01 06:27:30 pm
#####################################################

import numpy as np
from astropy.io import fits
import datetime, os, argparse
from . import __version__
from .caldb_config import CALDB_BASE_DIR


def write_lc(time_data, lc_data, time_bin, filter_sdd, outfile, clobber=True):
    hdu_list = []
    primary_hdu = fits.PrimaryHDU()
                                    
    hdu_list.append(primary_hdu)

    fits_columns = []
    col1 = fits.Column(name='TIME',format='1J',array=time_data)
    col2 = fits.Column(name='COUNTS',format='1E',array=lc_data)

    fits_columns.append(col1)
    fits_columns.append(col2)

    hdu_lc = fits.BinTableHDU.from_columns(fits.ColDefs(fits_columns))
    hdu_lc.name = 'RATE'

    hdu_list.append(hdu_lc)
                                                                       
    _hdu_list = fits.HDUList(hdus=hdu_list)

    hdu_lc.header['TSTART'] = time_data[0]
    hdu_lc.header['TSTOP'] = time_data[-1]
    hdu_lc.header['TIMEDEL'] = str(time_bin) #second
    hdu_lc.header['TIMZERO'] = 0
    hdu_lc.header['MJDREFI'] = 40587 # MJD REF of 1970-01-01 05:30:00
    hdu_lc.header['MJDREFF'] = 0.22916666651
    hdu_lc.header['TIMESYS'] = 'UTC'
    hdu_lc.header['TIMEREF'] = 'LOCAL'
    hdu_lc.header['TIMEUNIT'] = 's'
    date_obs = datetime.datetime.fromtimestamp(time_data[0]).strftime('%Y-%m-%d %H:%M:%S')
    date_end = datetime.datetime.fromtimestamp(time_data[-1]).strftime('%Y-%m-%d %H:%M:%S')
    hdu_lc.header['DATE-OBS'] = date_obs
    hdu_lc.header['DATE-END'] = date_end

    _HEADER_KEYWORDS = (
        ("EXTNAME", "RATE", "Extension name"),
        ("CONTENT", "LIGHT CURVE", "File content"),
        ("HDUCLASS", "OGIP    ", "format conforms to OGIP standard"),
        ("HDUVERS", "1.1.0   ", "Version of format (OGIP memo CAL/GEN/92-002a)"),
        (
            "HDUDOC",
            "OGIP memos CAL/GEN/92-007",
            "Documents describing the format",
        ),
        ("HDUVERS1", "1.0.0   ", "Obsolete - included for backwards compatibility"),
        ("HDUVERS2", "1.1.0   ", "Obsolete - included for backwards compatibility"),
        ("HDUCLAS1", "LIGHTCURVE", "Extension contains spectral data  "),
        ("HDUCLAS2", "TOTAL ", ""),
        ("HDUCLAS3", "COUNTS ", ""),
        ("FILTER", filter_sdd, "Filter used"),
    )

    data_header = _hdu_list[1].header
    
    for k in _HEADER_KEYWORDS:
        data_header.append(k)
    
    _hdu_list[1].header = data_header
    



    _PRIMARY_HEADER_KEYWORDS = (
        ("MISSION" , 'ADITYA L-1', 'Name of mission/satellite'),
        ("TELESCOP", 'AL1' , 'Name of mission/satellite'),
        ("INSTRUME", 'SoLEXS'      , 'Name of Instrument/detector'),
        ("ORIGIN"  , 'SoLEXSPOC'       , 'Source of FITS file'),
        ("CREATOR" , f'solexs_tools-{__version__}'  , 'Creator of file'),
        ("FILENAME", os.path.basename(outfile)            , 'Name of file'),
        ("CONTENT" , 'Type I PI file' , 'File content'),
        # ("VERSION" , __data_version__ , 'Data Product Version'),
        ("DATE", datetime.datetime.now().strftime("%Y-%m-%d"), 'Creation Date'),
    )
    
    primary_header = _hdu_list[0].header

    for k in _PRIMARY_HEADER_KEYWORDS:
        primary_header.append(k)

    _hdu_list[0].header = primary_header
        
    outfile = outfile[:-3] if outfile.endswith('.lc') else outfile
    _hdu_list.writeto(f'{outfile}.lc',overwrite=clobber)

    return f'{outfile}.lc'

def rebin_lc(lc_data, time_arr ,rebin_sec): #
    """lc_data: has to be counts per second"""
    extra_bins = len(lc_data) % rebin_sec
    if extra_bins != 0:
        lc_data = lc_data[:-extra_bins]
    new_bins = int(len(lc_data)/rebin_sec)
    new_lc_data = lc_data.reshape((new_bins, rebin_sec)).sum(axis=1)
    new_tm = np.arange(new_bins)*rebin_sec


    new_time_arr = []
    for ii in new_tm:
        new_time_arr.append(time_arr[int(ii)])

    new_lc_data = new_lc_data/rebin_sec #counts per second
    new_time_arr = np.array(new_time_arr) + rebin_sec/2

    return new_lc_data, new_time_arr


def solexs_genlc(spec_file, ene_low, ene_high, time_bin=None, outfile=None,clobber=True):
    hdu1 = fits.open(spec_file)

    if hdu1[0].header['CONTENT'] != 'Type II PHA file':
        raise TypeError('Input File is not Type II PHA file.')    
    
    data = hdu1[1].data

    time_solexs = data['TSTART']

    filter_sdd = hdu1[1].header['FILTER']
    ene_bins_file = os.path.join(CALDB_BASE_DIR,'ebounds',f'energy_bins_out_{filter_sdd}.dat')
    ene_bins = np.loadtxt(ene_bins_file)

    if ene_low < 2:
        raise ValueError('Lower energy limit cannot be less than 2 keV.')
    
    if ene_high > 22:
        raise ValueError('Higher energy limit cannot be more than 22 keV.')

    ch_low = np.where(ene_bins[:,0]>ene_low)[0][0]
    ch_high = np.where(ene_bins[:,1]<ene_high)[0][-1]

    ene_low_str = f'{ene_bins[ch_low,0]:.2f}'
    ene_high_str = f'{ene_bins[ch_high,1]:.2f}'

    lc_data = data['COUNTS'][:,ch_low:ch_high].sum(axis=1)

    if time_bin:
        lc_data, time_solexs = rebin_lc(lc_data,time_solexs,time_bin)
    else:
        time_bin = 1

    if outfile == None:
        pi_file_basename = os.path.basename(spec_file)
        pi_file_basename = pi_file_basename.split('.')[0]
        outfile = f'{pi_file_basename}_{ene_low_str}_{ene_high_str}keV.lc'

    outfile = write_lc(time_solexs,lc_data, time_bin, filter_sdd,outfile,clobber)

    return outfile


def solexs_genlc_cli():
    # Create the parser
    parser = argparse.ArgumentParser(description='Generate a light curve file from Level 1 PI spectrogram file (Type II) for a specified energy range.')

    # Add arguments
    parser.add_argument('-i','--infile', type=str, help='Path to the Level 1 PI spectrogram file (Type II)')
    parser.add_argument('-elo','--ene_low', type=float, help='Lower energy limit in keV')
    parser.add_argument('-ehi','--ene_high', type=float, help='Higher energy limit in keV')
    parser.add_argument('-tbin', '--time_bin', type=float, help='Time bin size in seconds', default=None)
    parser.add_argument('-o','--outfile', type=str, help='Output file name (optional)', default=None)
    parser.add_argument('-c','--clobber', type=bool, default= False, help='Overwrite existing file if it exists')

    # Parse arguments
    args = parser.parse_args()

    try:
        outfile_name = solexs_genlc(args.infile, args.ene_low, args.ene_high, args.time_bin, outfile=args.outfile, clobber=args.clobber)
        print(f"Output written to {outfile_name}.")
    except Exception as e:
        print(f"Error: {e}")


    