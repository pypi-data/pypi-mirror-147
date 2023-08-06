from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Hypixel API for Python'
LONG_DESCRIPTION = 'Easily use the Pypixel API from your terminal with PyPixel'

# Setting up
setup(
    name="MCPyPixelAPI",
    version=VERSION,
    author="William Allen",
    author_email="redacted@tocomail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)