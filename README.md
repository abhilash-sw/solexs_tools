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


Here’s a comprehensive **README** file for your `solexs_tools` package:

---

# SoLEXS_Tools

**SoLEXS_Tools** is a Python package for analyzing and processing data from the **SoLEXS** instrument on the **Aditya-L1 mission**. It provides tools for generating spectral data, converting time formats, and accessing calibration data.

---

## Features

- **Spectrum Generation**: Generate PI files with spectral data using `solexs-genspec`.
- **Time Conversions**:
  - `solexs-time2utc`: Convert Unix timestamps to UTC in ISO 8601 format.
  - `solexs-utc2time`: Convert UTC in ISO 8601 format to Unix timestamps.
- **Calibration Data Access**: Automatically resolves paths to ARF and RMF files within the CALDB directory.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/solexs_tools.git
   cd solexs_tools
   ```

2. Install the package:
   ```bash
   pip install .
   ```

3. For development purposes, use:
   ```bash
   pip install -e .
   ```

---

## CLI Commands

### `solexs-genspec`
Generate a PI file with spectral data for a specified time range.

**Usage**:
```bash
solexs-genspec <l1_pi_file> <tstart> <tstop> [-o OUTFILE] [--clobber]
```

**Arguments**:
- `<l1_pi_file>`: Path to the input L1 PI file.
- `<tstart>`: Start time in Unix timestamp.
- `<tstop>`: Stop time in Unix timestamp.

**Options**:
- `-o, --outfile`: Name of the output file.
- `--clobber`: Overwrite the output file if it exists.

**Example**:
```bash
solexs-genspec input_file.fits 1633046400 1633132800 -o output.pha --clobber
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
solexs-time2utc 1633046400
# Output: UTC Time: 2021-10-01T00:00:00+00:00
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
solexs-utc2time 2021-10-01T00:00:00
# Output: Unix Timestamp: 1633046400
```

---

## Configuration

The package automatically generates a configuration file, `caldb_config.py`, that defines the base directory for calibration data.

**Example**:
```python
from solexs_tools.caldb_config import CALDB_BASE_DIR

print(f"CALDB Base Directory: {CALDB_BASE_DIR}")
```

---

## File Structure

```plaintext
solexs_tools/
├── CALDB/
│   └── aditya-l1/
│       └── solexs/
│           └── data/
│               └── cpf/
│                   ├── arf/
│                   │   └── solexs_arf_SDD2.fits
│                   └── rmf/
│                       └── solexs_rmf_SDD2.rmf
├── solexs_tools/
│   ├── __init__.py
│   ├── solexs_genspec.py
│   ├── time_utils.py
│   ├── caldb_config.py
│   └── converters.py
├── setup.py
└── README.md
```

---

## Development

To add new features or fix bugs:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/solexs_tools.git
   cd solexs_tools
   ```

2. Install in development mode:
   ```bash
   pip install -e .
   ```

3. Run tests:
   ```bash
   pytest
   ```

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **SoLEXS Team**: For providing the specifications and datasets.
- **Aditya-L1 Mission**: India’s first solar mission by ISRO.

---

Feel free to modify the repository links, contributor details, and other specifics as needed. Let me know if you'd like further assistance!