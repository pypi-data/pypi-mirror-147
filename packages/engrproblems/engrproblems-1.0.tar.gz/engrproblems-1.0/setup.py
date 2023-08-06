import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="engrproblems",                     # This is the name of the package
    version="1.0",                        # The initial release version
    author="Hopalonghacksaw",                     # Full name of the author
    description="10 Engineering Problem Soultionns",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["engrproblems"],             # Name of the python package
    package_dir={'':'10EngrProblems/src'},     # Directory of the source code of the package
    install_requires=[]                     # Install other dependencies if any
)
