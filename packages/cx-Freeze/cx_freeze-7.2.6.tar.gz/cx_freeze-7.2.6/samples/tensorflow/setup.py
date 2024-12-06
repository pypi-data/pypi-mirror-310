"""A setup script to demonstrate the use of tensorflow.

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the script without Python.
"""

from cx_Freeze import setup

setup(
    name="test_tensorflow",
    version="0.1",
    description="cx_Freeze script to test tensorflow",
    executables=["test_tensorflow.py"],
    options={
        "build_exe": {
            "excludes": ["tkinter"],
        },
    },
)
