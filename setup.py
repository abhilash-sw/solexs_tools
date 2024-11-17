#####################################################
# @Author: SoLEXSPOC
# @Date:   2024-11-17 09:44:00 pm
# @email: sarwade@ursc.gov.in
# @File Name: setup.py
# @Project: solexs_tools
#
# @Last Modified time: 2024-11-17 10:35:58 pm
#####################################################

from setuptools import setup, find_packages

setup(
    name="solexs_tools",
    version="0.1",
    description="A toolkit for SoLEXS data analysis",
    author="Your Name",
    author_email="sarwade@ursc.gov.in",
    packages=find_packages(),
    package_data={
        # Include all files in CALDB
        "solexs_tools": [
            "CALDB/aditya-l1/solexs/data/cpf/*/*/*"
        ],
    },
    include_package_data=True,  # Ensures package_data is included
    install_requires=[
        "numpy",
        "astropy",
    ],
    entry_points={
        "console_scripts": [
            "solexs-genspec=solexs_tools.solexs_genspec:main",
            # "solexs-process=solexs_tools.process:main",
            # "solexs-summarize=solexs_tools.summarize:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
