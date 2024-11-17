#####################################################
# @Author: SoLEXSPOC
# @Date:   2024-11-17 09:27:23 pm
# @email: sarwade@ursc.gov.in
# @File Name: __init__.py
# @Project: solexs_tools
#
# @Last Modified time: 2024-11-17 10:25:59 pm
#####################################################

__version__ = 0.1

import os

def get_caldb_file(subpath):
    # Construct the full path to the data file
    # print(subpath)
    resource_path = os.path.join("CALDB", "aditya-l1", "solexs", "data", "cpf", subpath)
    # print(resource_path)
    basedir_path = os.path.join(os.path.dirname(__file__), '..')
    response_file_path = os.path.join(basedir_path, resource_path)
    print(response_file_path)
    return response_file_path
