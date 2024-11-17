#####################################################
# @Author: SoLEXSPOC
# @Date:   2024-11-17 09:27:23 pm
# @email: sarwade@ursc.gov.in
# @File Name: __init__.py
# @Project: solexs_tools
#
# @Last Modified time: 2024-11-17 10:56:48 pm
#####################################################

__version__ = 0.1

import os
import pkg_resources

def get_caldb_file2(subpath):
    # Construct the full path to the data file
    # print(subpath)
    resource_path = os.path.join("CALDB", "aditya-l1", "solexs", "data", "cpf", subpath)
    # print(resource_path)
    basedir_path = os.path.join(os.path.dirname(__file__), '..')
    response_file_path = os.path.join(basedir_path, resource_path)
    print(response_file_path)
    return response_file_path

def get_caldb_file(subpath):
    """
    Get the absolute path to a file in the CALDB directory.

    Args:
        subpath (str): Relative path within the CALDB directory (e.g., "response/response_file1.rsp").

    Returns:
        str: Absolute path to the file.
    """
    try:
        # Construct the full path to the data file
        resource_path = os.path.join("CALDB", "aditya-l1", "solexs", "data", "cpf", subpath)
        print(pkg_resources.resource_filename("solexs_tools", resource_path))
        return pkg_resources.resource_filename("solexs_tools", resource_path)
    except Exception as e:
        raise FileNotFoundError(f"File '{subpath}' not found in CALDB: {e}")