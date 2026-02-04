#####################################################
# @Author: SoLEXSPOC
# @Date:   2024-11-17 09:44:00 pm
# @email: sarwade@ursc.gov.in
# @File Name: setup.py
# @Project: solexs_tools
#
# @Last Modified time: 2026-02-04 09:39:13 pm
#####################################################

from setuptools import setup, find_packages
import os

setup(
    name="solexs_tools",
    version="1.3",
    description="A toolkit for SoLEXS data analysis",
    author="SoLEXSPOC",
    author_email="sarwade@ursc.gov.in",
    packages=find_packages(),
    # package_data={
    #     # Include all files in CALDB
    #     "solexs_tools": [
    #         "CALDB/*/*"
    #     ],
    # },
    include_package_data=True,  # Ensures package_data is included
    install_requires=[
        "numpy",
        "astropy",
        "scipy",
    ],
    entry_points={
        "console_scripts": [
            "solexs-genspec=solexs_tools.genspec:solexs_genspec_cli",
            "solexs-genmultispec=solexs_tools.genspec:solexs_genmultispec_cli",
            "solexs-genlc=solexs_tools.genlc:solexs_genlc_cli",
            "solexs-time2utc=solexs_tools.time_utils:solexs_time2utc_cli",
            "solexs-utc2time=solexs_tools.time_utils:solexs_utc2time_cli",
            "solexs-caldb-extract=solexs_tools.caldb_utils:solexs_caldb_extract_cli",
            "solexs-dtcorr=solexs_tools.deadtime:solexs_deadtime_correction_cli",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
