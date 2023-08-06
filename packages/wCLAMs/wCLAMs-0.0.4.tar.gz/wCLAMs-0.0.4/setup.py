from distutils.core import setup

setup(
    # Application name:
    name="wCLAMs",
    
    # Version number (initial):
    version="0.0.4",
    
    # Application author details:
    author="Zhang",
    author_email="oo@zju.edu.cn",
    
    # Packages
    packages=["app"],
    
    # Include additional files into the package
    include_package_data=True,
    
    # Details
    url="http://pypi.python.org/pypi/wCLAMs/",
    
    #
    license="LICENSE.txt",
    description="A GUI wrapper for pyCLAMs. Rewritten using Flask.",
    
    # long_description=open("README.md").read(),
    
    # Dependent packages (distributions)
    install_requires=[
        "flask",
    ],
)