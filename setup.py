#!python3
__author__ = 'Matjaz'
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {'packages': [],
					 'excludes': ['scipy', 'matplotlib'],
                     'include_files': ['style.qss']}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"
	# .. We want to run CMD by the side!
	# base = None

setup(  name = 'PresentationTimer',
        version = '0.1',
        description = 'Time presentations and q & a sessions.',
        options = {'build_exe': build_exe_options},
        executables = [Executable('timer.py', base=base)])