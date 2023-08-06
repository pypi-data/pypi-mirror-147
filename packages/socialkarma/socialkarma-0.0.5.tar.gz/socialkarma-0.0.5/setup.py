import setuptools

setuptools.setup(
    name="socialkarma",                     # This is the name of the package
    version="0.0.5",                        # The initial release version
    author="Chris Dang",                     # Full name of the author
    description="Social Karma Python SDK",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["socialkarma"],             # Name of the python package
    package_dir={'':'socialkarma/src'},     # Directory of the source code of the package
    install_requires=[]                     # Install other dependencies if any
)
