# **pytaglib**
[![CircleCI](https://img.shields.io/circleci/project/github/supermihi/pytaglib/master.svg)](https://circleci.com/gh/supermihi/pytaglib)
[![PyPI](https://img.shields.io/pypi/v/pytaglib.svg)](https://pypi.org/project/pytaglib/)

pytaglib is a [Python](http://www.python.org) audio tagging library. It is cross-platform, works with all Python versions, and is very simple to use yet fully featured:
 - [supports more than a dozen file formats](http://taglib.github.io) including mp3, flac, ogg, wma, and mp4,
 - support arbitrary, non-standard tag names,
 - support multiple values per tag.

pytaglib is a very thin wrapper (≈150 lines of [code](src/taglib.pyx)) around the fast and rock-solid [TagLib](http://taglib.github.io) C++ library.
## News
See the [Changelog](CHANGELOG.md).
## Get it
At first, you might need to install taglib with development headers. Ubuntu, Mint and other Debian-Based distributions:
        
        sudo apt install libtag1-dev

On a Mac, use HomeBrew:
        
        brew install taglib

Then install pytaglib with [pip](https://pip.pypa.io/en/stable/):

        pip install pytaglib


        
For other operating systems and more details, see [installation notes](#installation-notes) below.

## Usage

```python
>>> import taglib
>>> song = taglib.File("/path/to/my/file.mp3")
>>> song.tags
{'ARTIST': ['piman', 'jzig'], 'ALBUM': ['Quod Libet Test Data'], 'TITLE': ['Silence'], 'GENRE': ['Silence'], 'TRACKNUMBER': ['02/10'], 'DATE': ['2004']}

>>> song.length
239
>>> song.tags["ALBUM"] = ["White Album"] # always use lists, even for single values
>>> del song.tags["DATE"]
>>> song.tags["GENRE"] = ["Vocal", "Classical"]
>>> song.tags["PERFORMER:HARPSICHORD"] = ["Ton Koopman"] 
>>> song.save()
```
For detailed API documentation, use the docstrings of the `taglib.File` class or view the [source code](src/taglib.pyx) directly.


**Note:** pytaglib uses unicode strings (type `str` in Python 3 and `unicode` in Python 2) for both tag names and values. The library converts byte-strings to unicode strings on assignment, but it is recommended to provide unicode strings only to avoid encoding problems.


## `pyprinttags`
This package also installs the `pyprinttags` script. It takes one or more files as
command-line parameters and will display all known metadata of that files on the terminal.
If unsupported tags (a.k.a. non-textual information) are found, they can optionally be removed
from the file.

## Installation Notes

* Ensure that `pip` is installed and points to the correct Python version
  - on Windows, be sure to check *install pip* in the Python installer
  - on Debian/Ubuntu/Mint, install `python3-pip` (and/or `python-pip`)
  - you might need to type, e.g., `pip-3` to install pytaglib for Python 3 if your system's default is Python 2.7.
* For Windows users, there are some precompiled binary packages (wheels). See the [PyPI page](https://pypi.python.org/pypi/pytaglib) for a list of supported Python versions.
* If no binary packages exists, you need to have both Python and taglib installed with development headers (packages `python3-dev` (or `python-dev`) and `libtag1-dev` for debian / ubuntu and derivates, `python-devel` and `taglib-devel` for fedora and friends, `brew install taglib` on OS X).


### Linux: Distribution-Specific Packages
* Debian- and Ubuntu-based linux flavors have binary packages for the Python 3 version, called `python3-taglib`. Unfortunatelly, they are heavily outdated, so you should instally the recent version via `pip` whenever possible.
* For Arch users, there is a [package](https://aur.archlinux.org/packages/python-pytaglib/) in the user repository (AUR).

### Manual Compilation: General
You can download or checkout the sources and compile manually:

        python setup.py build
        python setup.py test  # optional, run unit tests
        sudo python setup.py install


**Note**: The `taglib` Python extension is built from [`taglib.cpp`](src/taglib.cpp) which in turn is
auto-generated by [Cython](http://www.cython.org) from [`taglib.pyx`](src/taglib.pyx).
To regenerate the `taglib.cpp` after making changes to `taglib.pyx`, set the environment variable `PYTAGLIB_CYTHONIZE` to `1` before calling `setup.py` or `pip`.

### Compilation: Windows

Install MS Visual Studio Build Tools (or the complete IE) and include the correct compiler version as detailed [here](https://wiki.python.org/moin/WindowsCompilers). Also enable *cmake* in the Visual Studio Installer.

Then, open a powershell console in the *pytaglib* repository and run: `windows\build.ps1`. This will download and compile taglib and create a binary windows wheel in the `dist` folder.


## Contact
For bug reports or feature requests, please use the
[issue tracker](https://github.com/supermihi/pytaglib/issues) on GitHub. For anything else, contact
me by [email](mailto:michaelhelmling@posteo.de).
