# SoLEXS_Tools
**SoLEXS_Tools** is a Python package for analyzing and processing data from the **SoLEXS** (Solar Low Energy X-ray Spectrometer) instrument on the **Aditya-L1** mission. It provides tools for SoLEXS data analysis. 

---

## Requirements

Before installing **SoLEXS_Tools**, ensure that the following dependencies are met:

1. **Python 3.6 or Higher**
   **Check Python Version**:
   ```bash
   python3 --version
   ```

2. **XSPEC**
   - XSPEC is required for advanced spectral analysis. Install XSPEC as part of the HEASoft suite from [HEASoft's official website](https://heasarc.gsfc.nasa.gov/xanadu/xspec/).

   **Verify XSPEC Installation**:
   Open a terminal and type:
   ```bash
   xspec
   ```
   If XSPEC starts without errors, the installation is successful.

---

## Installation
```bash
tar xvf solexs_tools-0.1.tar.gz
cd solexs_tools
pip install .
```

## CLI Commands

### `solexs-genspec`
Generate a type-I PI file with spectral data for a specified time range.

**Usage**:
```bash
solexs-genspec -i <l1_pi_file> -tstart <tstart> -tstop <tstop> [-o <outfile>] [--clobber <True/False>]
```

**Arguments**:
- `<l1_pi_file>`: Path to the Level 1 PI spectrogram file (Type II)
- `<tstart>`: Start time in Unix seconds
- `<tstop>`: Stop time in Unix seconds
- `<l1_gti_file>`: Path to the Level 1 Good Time Interval File

**Options**:
- `-o, --outfile`: Name of the output file.
- `--clobber`: Overwrite the output file if it exists.

**Example**:
```bash
solexs-genspec -i AL1_SOLEXS_20240212_SDD2_L1.pi.gz -tstart 1707715800 -tstop 1707715860 -gti AL1_SOLEXS_20240212_SDD2_L1.gti.gz
```

---

### `solexs-time2utc`
Convert a Unix timestamp to UTC in ISO 8601 format.

**Usage**:
```bash
solexs-time2utc <unix_time>
```

**Arguments**:
- `<unix_time>`: Unix timestamp to convert.

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
- `<utc_time>`: UTC time in ISO 8601 format.

**Example**:
```bash
solexs-utc2time 2024-02-12T11:00:00
# Output: Unix Timestamp: 1707715800
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
