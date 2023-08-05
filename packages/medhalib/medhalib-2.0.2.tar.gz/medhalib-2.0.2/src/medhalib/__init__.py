import site
import os.path

# read version details from version.txt
def read_version():
    version_file = """Version: 2.0.1 [Date: 2022-04-17 18:46:53.688520]"""
    return version_file

__version__=read_version()