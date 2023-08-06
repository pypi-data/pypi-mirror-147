from setuptools import setup, find_packages
from pathlib import Path
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ciscouctoolkit",
    version="2.114",
    author="Michael Ralston",
    author_email="michaelaaralston2@gmail.com",
    description="Cisco CUCM AXL Library, PAWS, DIME, IMP AXL, Log Collection.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    url="https://github.com/MichaelRalston98/ciscouctoolkit",
    keywords=["Cisco", "Call Manager", "CUCM", "AXL", "VoIP"],
    packages=["UCToolkit"],
    package_data={"UCToolkit": ["*.wsdl", "*.xsd", "CUCM/*/*/*", "IMP/*/*/*", "paws/*"],},
    install_requires=[
        'setuptools==40.0.0',
        'xmltodict',
        'requests',
        'zeep',
        'lxml',
        'urllib3',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)