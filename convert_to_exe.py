from distutils.core import setup
import py2exe, sys, os, pygame

sys.argv.append('py2exe')

setup(
    py_modules=[],
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    windows = [{'script': r"C:\\Users\\ilgaz\Documents\\Fizik Projesi\\main.py"}],
    zipfile = None,
)