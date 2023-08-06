from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


VERSION = '0.0.1'
DESCRIPTION = 'ENGR 103 HW package, my first Programming package '


# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="engrproblems",
        version=VERSION,
        author="Ryan Hopkins",
        author_email="hopkinsr@oregonstate.edu",
        description=DESCRIPTION,
        long_description=long_description,      # Long description read from the the readme file
        long_description_content_type="text/markdown",
        packages=find_packages(),
        install_requires=[], # add any additional packages that
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'first package','Engr 103','OSU','ENGR 103 HW'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
