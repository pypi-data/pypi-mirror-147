from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'Hypixel API for Python'
LONG_DESCRIPTION = 'Easily use the Hypixel API from your terminal with PyPixel, full documentation is on my Github: https://github.com/lamaprogramer/PyPixel'

# Setting up
setup(
    name="MCPyPixelAPI",
    version=VERSION,
    author="William",
    author_email="redacted@tocomail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'hypixel', 'minecraft', 'api', 'webapi'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)