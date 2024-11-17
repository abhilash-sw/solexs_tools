#####################################################
# @Author: SoLEXSPOC
# @Date:   2024-11-17 09:27:23 pm
# @email: sarwade@ursc.gov.in
# @File Name: __init__.py
# @Project: solexs_tools
#
# @Last Modified time: 2024-11-17 09:40:57 pm
#####################################################

__version__ = 0.1

import os
import pkg_resources  # For accessing package data

def get_caldb_file(subpath):
    try:
        # Construct the full path to the data file
        resource_path = os.path.join("CALDB", "aditya-l1", "solexs", "data", "cpf", subpath)
        return pkg_resources.resource_filename("solexs_tools", resource_path)
    except Exception as e:
        raise FileNotFoundError(f"File '{subpath}' not found in CALDB: {e}")