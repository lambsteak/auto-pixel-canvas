import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"], "excludes": ["tkinter"],
                     'include_files': ['captcha.png', 'fig.png', 'ok.png',
                                       'ok2.png', 'skipad.png', 'commcon.py']}

base = None
if sys.platform == "win32":
    base = "console"

setup(name="auto_pixelgrad",
      version="0.1",
      description="Build the Pixelgrag automatically!",
      options={"build_exe": build_exe_options},
      executables=[Executable("auto_pixel.py", base=base)])
