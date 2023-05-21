from distutils.core import setup
import subprocess
try:
    import py2exe
except:
    subprocess.Popen("python -m pip install py2exe",shell=True)
import sys, os, pygame

sys.argv.append('py2exe')

setup(
    py_modules=[],
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    windows = [{'script': r"PATH_TO_MAIN"}],
    zipfile = None,
)
