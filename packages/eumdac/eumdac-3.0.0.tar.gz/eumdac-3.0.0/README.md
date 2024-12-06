# EUMDAC - EUMETSAT Data Access Client

**EUMDAC** is the **EUM**ETSAT **D**ata **A**ccess **C**lient. It provides simple access to the EUMETSAT data of all satellite missions. As a **Python library**, it comes with many methods and helpers to use EUMETSATs APIs and services, like Data Store and Data Tailor. As a **CLI**, it provides a variety of useful command line utilities for data search, translation and processing.

Please consult the following documentation for more information:
- [EUMDAC User Guide](https://user.eumetsat.int/resources/user-guides/eumetsat-data-access-client-eumdac-guide) - Installing and using the CLI and library.
- [EUMDAC API Reference](https://usc.tools.eumetsat.int/docs/eumdac/) - Detailed information on classes, functions, and modules, including method descriptions and parameter usage.


## Prerequisites
 
You will need a python environment to run the library implementation of this code. EUMDAC requires Python 3.7 or higher. We recommend that you install the latest Anaconda Python distribution for your operating system (https://www.anaconda.com/). No prerequisites are identified for running the CLI binary.

## Installing the EUMDAC library and CLI

### Installing with PIP

The EUMDAC Python package is available through [PyPI](https://pypi.org/):
```bash
pip install eumdac
```

### Installing with Conda

To install EUMDAC on the Anaconda Python distribution, please visit the [EUMETSAT conda-forge page](https://anaconda.org/Eumetsat/repo) for install instructions.
```bash
conda install -c eumetsat-forge eumdac
```

### Installing from source

To install EUMDAC from the development source, clone the repository and install it locally.

```bash
git clone https://gitlab.eumetsat.int/eumetlab/data-services/eumdac.git
cd eumdac
pip install .
```

## Using the EUMDAC CLI binaries (no installation required)
If an installation of EUMDAC is not possible due to missing technical prerequisites, we recommend to use our binaries. These executable applications allow you to use all the functions of the CLI without installation. 

The binaries are available for Windows, Linux and Mac in the [Releases section](https://gitlab.eumetsat.int/eumetlab/data-services/eumdac/-/releases).

You can find more information in the [EUMDAC User Guide](https://user.eumetsat.int/resources/user-guides/eumetsat-data-access-client-eumdac-guide#ID-Command-Line-guide).

## Contributing
If you feel like something is missing, should work differently or you find a bug in EUMDAC you are encouraged to provide feedback to the development team. Please contact us via the [EUMETSAT User Support Helpdesk](mailto:ops@eumetsat.int) if you have suggestions or questions.

## Authors
See AUTHORS.txt for the list of contributors.

## Dependencies
pyyaml,     License: MIT (LICENSE_MIT.txt),              Copyright 2019 Ingy döt Net,    info: https://anaconda.org/conda-forge/pyyaml/ \
requests,   License: Apache-2.0 (LICENSE_APACHE_v2.txt), Copyright 2014 Kenneth Reitz,   info: https://anaconda.org/conda-forge/requests  \
responses,  License: Apache-2.0 (LICENSE_APACHE_v2.txt), Copyright 2015 David Cramer,    info: https://anaconda.org/conda-forge/responses  \
setuptools, License: MIT (LICENSE_MIT.txt),              Copyright 2020 Jason R. Coombs, info: https://anaconda.org/conda-forge/setuptools  

## License
 
This code is licensed under an MIT license. See file LICENSE.txt for details on the usage and distribution terms. No dependencies are distributed as part of this package.

All product names, logos, and brands are property of their respective owners. All company, product and service names used in this website are for identification purposes only.
