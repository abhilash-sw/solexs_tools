#####################################################
# @Author: SoLEXSPOC
# @Date:   2024-11-15 09:00:07 am
# @email: sarwade@ursc.gov.in
# @File Name: solexs_genspec.py
# @Project: solexs_tools
#
# @Last Modified time: 2024-11-17 09:42:34 pm
#####################################################

import argparse
import datetime
from astropy.io import fits
import numpy as np
import os

from . import __version__, get_caldb_file


def solexs_genspec(spec_file,tstart,tstop,outfile=None,clobber=True): # times in unix seconds

    hdu1 = fits.open(spec_file)

    if hdu1[0].header['CONTENT'] != 'Type II PHA file':
        raise TypeError('Input File is not Type II PHA file.')

    hdu=fits.BinTableHDU.from_columns(hdu1[1].columns)

    data=hdu.data

    time_solexs = data['TSTART']
    # tbinsize=(data['TSTOP'][0]-data['TSTART'][0])
    
    exposure=data['EXPOSURE']

    inds = (time_solexs >= tstart) & (time_solexs < tstop)

    data_f = data[inds]

    channel = data_f[0][3]
    n_ch = len(channel)
    spec_data = np.zeros(n_ch)
    stat_err = np.zeros(n_ch)
    sys_err = np.zeros(n_ch)
    exposure = 0

    for di in data_f:
        spec_data = spec_data + di[4]
        # stat_err = stat_err + np.sqrt(di[4])
        # sys_err = sys_err
        exposure = exposure + di[5]

    stat_err = np.sqrt(spec_data)

    grp = np.ones(512)

    for i in range(168,512):
        if i%2 == 0:
            grp[i] = 1
        else:
            grp[i] = -1    
    
    # writing file
    hdu_list = []
    primary_hdu = fits.PrimaryHDU()
                                    
    hdu_list.append(primary_hdu)

    fits_columns = []
    col1 = fits.Column(name='CHANNEL',format='1J',array=channel)
    col2 = fits.Column(name='COUNTS',format='1E',array=spec_data)
    col3 = fits.Column(name='STAT_ERR',format='1E',array=stat_err)
    col4 = fits.Column(name='SYS_ERR',format='1E',array=sys_err)
    col5 = fits.Column(name='GROUPING',format='1J',array=grp)

    fits_columns.append(col1)
    fits_columns.append(col2)
    fits_columns.append(col3)
    fits_columns.append(col4)
    fits_columns.append(col5)

    hdu_pha = fits.BinTableHDU.from_columns(fits.ColDefs(fits_columns))
    hdu_pha.name = 'SPECTRUM'
                                                                       
    hdu_list.append(hdu_pha)
                                                                       
    _hdu_list = fits.HDUList(hdus=hdu_list)

    tstart_dt = datetime.datetime.fromtimestamp(tstart)
    tstop_dt = datetime.datetime.fromtimestamp(tstop)
    
    filter_sdd = hdu1[1].header['FILTER']

    _hdu_list[1].header.set('TSTART',tstart_dt.isoformat())
    _hdu_list[1].header.set('TSTOP',tstop_dt.isoformat())
    _hdu_list[1].header.set('TIMESYS', 'UTC')
    _hdu_list[1].header.set('EXPOSURE',f'{exposure:.4f}')

    
    _HEADER_KEYWORDS = (
        ("EXTNAME", "SPECTRUM", "Extension name"),
        ("CONTENT", "OGIP PHA data", "File content"),
        ("MISSION" , 'ADITYA L-1', 'Name of mission/satellite'),
        ("TELESCOP", 'AL1' , 'Name of mission/satellite'),
        ("INSTRUME", 'SoLEXS'      , 'Name of Instrument/detector'),        
        ("HDUCLASS", "OGIP    ", "format conforms to OGIP standard"),
        ("HDUVERS", "1.1.0   ", "Version of format (OGIP memo CAL/GEN/92-002a)"),
        (
            "HDUDOC",
            "OGIP memos CAL/GEN/92-002 & 92-002a",
            "Documents describing the forma",
        ),
        ("HDUVERS1", "1.0.0   ", "Obsolete - included for backwards compatibility"),
        ("HDUVERS2", "1.1.0   ", "Obsolete - included for backwards compatibility"),
        ("HDUCLAS1", "SPECTRUM", "Extension contains spectral data  "),
        ("HDUCLAS2", "TOTAL ", ""),
        ("HDUCLAS3", "COUNT ", ""),
        ("HDUCLAS4", "TYPE:I ", ""),
        ("FILTER", filter_sdd, "Filter used"),
        ('RESPFILE', 'solexs_gaussian_SDD2_512.rmf'),
        ('ANCRFILE', 'solexs_arf_SDD2.fits'),
        ('BACKFILE','None'),        
        ("CHANTYPE", "PI", "Channel type"),
        ("POISSERR", False, "Are the rates Poisson distributed"),
        ("DETCHANS", n_ch, "Number of channels"),
        ("CORRSCAL", 1.0, ""),
        ("AREASCAL", 1.0, ""),
        ("BACKSCAL", 1.0, ""),
        ("SYS_ERR", 1, "Systematic error to be applied"),
#         ("QUALITY", 0, "Data quality flag"),
        ("GROUPING", 1, "Whether data is grouped"),
        ("TLMIN", 0, "Minimum legal value for 'CHANNEL' column"),
        ("TLMAX", n_ch-1, "Maximum legal value for 'CHANNEL' column"),
    )
    
    data_header = _hdu_list[1].header
    
    for k in _HEADER_KEYWORDS:
        data_header.append(k)
    
    _hdu_list[1].header = data_header
    


    if outfile == None:
        pi_file_basename = os.path.basename(spec_file)
        pi_file_basename = pi_file_basename.split('.')[0]
        outfile = pi_file_basename + '_' + tstart_dt.strftime('%H%M%S') + '_' + tstop_dt.strftime('%H%M%S')

    _PRIMARY_HEADER_KEYWORDS = (
        ("MISSION" , 'ADITYA L-1', 'Name of mission/satellite'),
        ("TELESCOP", 'AL1' , 'Name of mission/satellite'),
        ("INSTRUME", 'SoLEXS'      , 'Name of Instrument/detector'),
        ("ORIGIN"  , 'SoLEXSPOC'       , 'Source of FITS file'),
        ("CREATOR" , f'solexs_genspec-{__version__}'  , 'Creator of file'),
        ("FILENAME", outfile            , 'Name of file'),
        ("CONTENT" , 'Type I PI file' , 'File content'),
        # ("VERSION" , __data_version__ , 'Data Product Version'),
        ("DATE", datetime.datetime.now().strftime("%Y-%m-%d"), 'Creation Date'),
    )
    
    primary_header = _hdu_list[0].header

    for k in _PRIMARY_HEADER_KEYWORDS:
        primary_header.append(k)

    _hdu_list[0].header = primary_header
        

    _hdu_list.writeto(f'{outfile}.pi',overwrite=clobber)
    return f'{outfile}.pi'


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Integrate a SoLEXS Type II PI spectrogram to produce a Type I PI spectrum file.')

    # Add arguments
    parser.add_argument('-i','--infile', type=str, help='Path to the Level 1 PI spectrogram file (Type II)')
    parser.add_argument('-tstart', type=int, help='Start time in Unix seconds')
    parser.add_argument('-tstop', type=int, help='Stop time in Unix seconds')
    parser.add_argument('-o','--outfile', type=str, help='Output file name (optional)', default=None)
    parser.add_argument('-c','--clobber', type=bool, default=True, help='Overwrite existing file if it exists')

    # Parse arguments
    args = parser.parse_args()

    # Call the function with the parsed arguments
    try:
        outfile_name = solexs_genspec(args.infile, args.tstart, args.tstop, outfile=args.outfile, clobber=args.clobber)
        print(f"Output written to {outfile_name}.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()