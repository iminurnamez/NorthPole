import sys
from cx_Freeze import setup, Executable

base = None 
if sys.platform == "win32":
    base = "Win32GUI"
   
exe = Executable(script="northpole.py", base=base)
 
include_files=["resources/music", "resources/graphics", "resources/sound",
                     "resources/fonts", "resources/mtkringle.json"]
includes=[]
excludes=[]
packages=[]

setup(version="0.1",
         description="A Christmas-themed tycoon game",
         author="iminurnamez",
         name="North Pole Tycoon",
         options={"build_exe": {"includes": includes, "include_files": include_files, "packages": packages, "excludes": excludes}},
         executables=[exe])

