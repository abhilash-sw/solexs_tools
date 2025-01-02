# SoLEXS_Tools
**SoLEXS_Tools** is a Python package developed to facilitate the processing and preparation of data from the **SoLEXS** (Solar Low Energy X-ray Spectrometer) instrument on the **Aditya-L1** mission. It provides essential tools and utilities generating and managing spectral data and calibration files, enabling users to perform spectral analysis using specialized tools such as **XSPEC** or **Sherpa**. The package includes SoLEXS calibration database (**CALDB**), which provides essential calibration files such as Auxiliary Response File (**ARF**) and Redistribution Matrix File (**RMF**).
---

## Requirements

Before installing **SoLEXS_Tools**, ensure that the following dependencies are met:

1. **Python 3.6 or Higher**
   **Check Python Version**:
   ```bash
   python3 --version
   ```

2. External Python Packages
   **NumPy, Astropy**
   Install the dependencies using pip:
   ```bash
   pip install numpy astropy
   ```

## Tools for Spectral Analysis
1. **XSPEC**
   For spectral fitting and analysis. Install XSPEC as part of the HEASoft suite from [HEASoft's official website](https://heasarc.gsfc.nasa.gov/xanadu/xspec/).

   **Verify XSPEC Installation**:
   Open a terminal and type:
   ```bash
   xspec
   ```
   If XSPEC starts without errors, the installation is successful.

2. **Sherpa**
   An alternative Python-based spectral fitting and analysis tool available [here](https://sherpa.readthedocs.io).
---

## Installation
```bash
tar xvf solexs_tools-m.n.tar.gz
cd solexs_tools
python setup.py build
python setup.py install
```

## CLI Commands

### `solexs-time2utc`
Convert a Unix timestamp to UTC in ISO 8601 format.

**Usage**:
```bash
solexs-time2utc <unix_time>
```

**Arguments**:
- `<unix_time>`: Unix timestamp to convert

**Example**:
```bash
solexs-time2utc 1707715800
# Output: UTC Time: 2024-02-12T11:00:00
```

---

### `solexs-utc2time`
Convert UTC in ISO 8601 format to a Unix timestamp.

**Usage**:
```bash
solexs-utc2time <utc_time>
```

**Arguments**:
- `<utc_time>`: UTC time in ISO 8601 format

**Example**:
```bash
solexs-utc2time 2024-02-12T11:00:00
# Output: Unix Timestamp: 1707715800
```

---

### `solexs-genlc`
Generate a light curve file from Level 1 PI spectrogram file (Type II) for a specified energy range.

**Usage**:
```bash
solexs-genlc -i <l1_pi_file> -elo <ene_low> -ehi <ene_high> [-tbin <time_bin>] [-o <outfile>] [--clobber <True/False>]
```

**Arguments**:
- `<l1_pi_file>`: Path to the Level 1 PI spectrogram file (Type II)
- `<ene_low>`: Lower energy limit in keV
- `<ene_high>`: Higher energy limit in keV

**Options**:
- `<time_bin>`: Time bin size in seconds (Default set to one second)
- `-o, --outfile`: Name of the output file
- `-c, --clobber`: Overwrite the output file if it exists

**Example**:
```bash
solexs-genlc -i AL1_SOLEXS_20240212_SDD2_L1.pi.gz -elo 3 -ehi 10
```

---

### `solexs-genspec`
Generate a type-I PI spectral file from Level 1 PI spectrogram file (Type II) for a specified time range.

**Usage**:
```bash
solexs-genspec -i <l1_pi_file> -tstart <tstart> -tstop <tstop> -gti <l1_gti_file> [-o <outfile>] [--clobber <True/False>]
```

**Arguments**:
- `<l1_pi_file>`: Path to the Level 1 PI spectrogram file (Type II)
- `<tstart>`: Start time in Unix seconds
- `<tstop>`: Stop time in Unix seconds
- `<l1_gti_file>`: Path to the Level 1 Good Time Interval File

**Options**:
- `-o, --outfile`: Name of the output file
- `-c, --clobber`: Overwrite the output file if it exists

**Example**:
```bash
solexs-genspec -i AL1_SOLEXS_20240212_SDD2_L1.pi.gz -tstart 1707715800 -tstop 1707715860 -gti AL1_SOLEXS_20240212_SDD2_L1.gti.gz
```

---

### `solexs-genmultispec`
Generate multiple type-I PI spectral files from Level 1 PI spectrogram file (Type II) for a specified time range and time binning.

**Usage**:
```bash
solexs-genmultispec -i <l1_pi_file> -tstart <tstart> -tstop <tstop> -tbin <time_bin> -gti <l1_gti_file> [-o <outdir>] [--clobber <True/False>]
```

**Arguments**:
- `<l1_pi_file>`: Path to the Level 1 PI spectrogram file (Type II)
- `<tstart>`: Start time in Unix seconds
- `<tstop>`: Stop time in Unix seconds
- `<time_bin>`: Time bin size in seconds
- `<l1_gti_file>`: Path to the Level 1 Good Time Interval File

**Options**:
- `-o, --outdir`: Name of the output directory
- `-c, --clobber`: Overwrite the output file if it exists

**Example**:
```bash
solexs-genmultispec -i AL1_SOLEXS_20240212_SDD2_L1.pi.gz -tstart 1707715800 -tstop 1707715860 -tbin 10 -gti AL1_SOLEXS_20240212_SDD2_L1.gti.gz
```

---


## Configuration

The package automatically generates a configuration file, `caldb_config.py`, that defines the path to the directory for calibration data.

**Example**:
```python
from solexs_tools.caldb_config import CALDB_BASE_DIR

print(f"CALDB Base Directory: {CALDB_BASE_DIR}")
```

---

## Example Jupyter Notebook
The package includes an example notebook that demonstrates how to perform spectral fitting of SoLEXS data using XSPEC.