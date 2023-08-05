import site
import os.path

# read version details from version.txt
def read_version():
    version_file = """Version: 2.0.3 [Date: 2022-04-17 19:09:03.258586]"""
    return version_file

__version__=read_version()