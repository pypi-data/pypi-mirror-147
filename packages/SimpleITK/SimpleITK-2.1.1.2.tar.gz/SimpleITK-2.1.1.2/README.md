# SimpleITKPythonPackage

This project provides a `setup.py` script that can build, install, and package SimpleITK for Python. [SimpleITK](http://www.simpleitk.org) is a simplified programming layer on top of the [Insight Segmentation and Registration Toolkit](https://itk.org) (ITK).  ITK is an open-source, cross-platform system that provides developers with an extensive suite of software tools for image analysis.

SimpleITK is available for binary downloads from [PyPI](https://pypi.python.org/pypi/SimpleITK) for many common platforms. Also a source distribution is available of this repository which may be used when an appropriate binary [wheel](http://pythonwheels.com) is not available.

To install SimpleITK:

```bash
pip install SimpleITK
```

## Installing SimpleITK for Python from the Python Packaging Source

```bash
pip install SimpleITK
```

### Prerequisites

Building *requires*:
* [CMake](https://cmake.org)
* Git
* C++ Compiler - Platform specific requirements are summarized in [scikit-build documentation](http://scikit-build.readthedocs.io).
* Python
  * pip >= 9.0.0
  * scikit-build >= 0.5.0
  
Please ensure that `pip` and `scikit-build` are up to date and are a recent version.

*Optional*:

If CMake is not already available on you system it can be installed with pip. Additionally, the [Ninja](https://ninja-build.org) build tool is recommened for it's parallel build efficiency. These can be easily installed with:

```bash
pip install cmake ninja
```

### Compilations and Installation from Github

SimpleITK can be compiled and install directly from the github repository:

```bash
pip install git+https://github.com/SimpleITK/SimpleITKPythonPackage.git -v
```

### Compilation and Installation from Source Distribution

Alternatively, SimpleITK for Python can be compiled and installed from the SimpleITKPythonPackage python source distribution.

```bash
pip install SimpleITKPythonPackage-1.0.0.tar.gz
```

The source distributions are available from [PyPI](https://pypi.python.org/pypi/SimpleITK) and [Source Forge](https://sourceforge.net/projects/simpleitk/files/SimpleITK/1.0.0/Python). They are labeled as `SimpleITKPythonPackages` in the Python sub-directory as opposed to just `SimpleITK` for the source archive of the general SimpleITK repository.



## Miscellaneous
Written by Jean-Christophe Fillion-Robin from Kitware Inc.

It is covered by the Apache License, Version 2.0:

http://www.apache.org/licenses/LICENSE-2.0

For more information about SimpleITK, visit http://simpleitk.org

For more information about ITK, visit http://itk.org

