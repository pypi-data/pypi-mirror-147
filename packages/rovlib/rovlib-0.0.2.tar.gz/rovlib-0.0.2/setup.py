from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'ROV control and image library'
LONG_DESCRIPTION = "A custom library that exactly fits our needs, be it programmatically controlling a Remote Operated Vehicle (ROV) or processing image data from the on-board cameras, it's got you covered."
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Natural Language :: English',
    'Operating System :: POSIX :: Linux',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.9'
]
# Setting up
setup(
    name="rovlib",
    version=VERSION,
    url='https://github.com/RobEn-AAST/ROV-LIB',
    author="karimkohel & abbasebnfernas",
    author_email="<kareemkohel@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    py_modules=['rovlib.cameras', 'rovlib.control'],
    packages=['rovlib'],
    install_requires=['opencv-python', 'pymavlink'],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets', 'mavlink', 'rov', 'control', 'ardusub'],
    classifiers=classifiers
)