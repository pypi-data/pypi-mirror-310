"""A simple setup script to create an executable using numexpr/mkl. This also
demonstrates how to use excludes to get minimal package size.

test_mkl.py is a very simple type of numexpr application using mkl.

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the application.
"""

from cx_Freeze import setup

options = {
    "build_exe": {
        # exclude packages that are not really needed
        "excludes": ["tkinter", "unittest", "email", "xml", "pydoc"],
    },
}

setup(
    name="test_mkl",
    version="0.1",
    description="Sample numexpr script",
    executables=["test_mkl.py"],
    options=options,
)
