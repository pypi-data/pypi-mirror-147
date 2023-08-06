# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfk',
 'pyfk.config',
 'pyfk.gf',
 'pyfk.gf.cuda',
 'pyfk.sync',
 'pyfk.taup',
 'pyfk.tests',
 'pyfk.tests.config',
 'pyfk.tests.gf',
 'pyfk.tests.sync',
 'pyfk.tests.taup',
 'pyfk.utils']

package_data = \
{'': ['*'],
 'pyfk.tests': ['data/*',
                'data/hk_gf/*',
                'data/sync_filter/*',
                'data/sync_prem_ep/*',
                'data/sync_prem_gcmt/*',
                'data/sync_prem_sf/*',
                'data/sync_receiver_deeper/*',
                'data/sync_smth/*']}

install_requires = \
['Cython>=0.29.28,<0.30.0', 'cysignals>=1.11.2,<2.0.0', 'obspy>=1.3.0,<2.0.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['numpy>=1.21.5,<2.0.0',
                                                         'scipy>=1.7.0,<2.0.0'],
 ':python_version >= "3.8" and python_version < "3.10"': ['numpy>=1.22.3,<2.0.0',
                                                          'scipy>=1.8.0,<2.0.0'],
 'mpi': ['mpi4py>=3.1.3,<4.0.0']}

setup_kwargs = {
    'name': 'pyfk',
    'version': '0.3.0',
    'description': "Pyfk is the python version of FK used to calculate the Green's function and the synthetic waveforms for the 1D Earth model.",
    'long_description': 'PyFK\n==========\n\n.. image:: https://github.com/ziyixi/pyfk/workflows/pyfk/badge.svg\n    :target: https://github.com/ziyixi/pyfk/actions\n\n.. image:: https://codecov.io/gh/ziyixi/pyfk/branch/master/graph/badge.svg?token=5EL7IDTYLJ\n    :target: https://codecov.io/gh/ziyixi/pyfk\n\n.. image:: https://img.shields.io/badge/docs-dev-blue.svg\n    :target: https://ziyixi.github.io/pyfk/\n\n.. image:: https://badge.fury.io/py/pyfk.svg\n    :target: https://badge.fury.io/py/pyfk\n\n.. image:: https://anaconda.org/ziyixi/pyfk/badges/version.svg\n    :target: https://anaconda.org/ziyixi/pyfk\n\n.. image:: https://anaconda.org/ziyixi/pyfk/badges/platforms.svg\n    :target: https://github.com/ziyixi/pyfk\n\n.. placeholder-for-doc-index\n\nAbout\n-------------\n\nPyFK is the python port of `FK <http://www.eas.slu.edu/People/LZhu/home.html>`__ used to calculate the Green\'s function and the synthetic waveforms for the 1D Earth model.\n\nThe main features of this package are:\n\n* Compute the Green\'s function for the explosion, single force, and double couple source using the frequency-wavenumber method.\n* Compute the static displacements and corresponding Green\'s function.\n* Compute the synthetic waveforms by convolving Green\'s function with the seismic source.\n* Use the seismic data format of Obspy, which is easy to perform the signal processing.\n\nAnd the package is unique as:\n\n* all the code is written in pure python, and it\'s compatible with Unix-like systems including Mac and Linux. The Windows is not supported, as the package uses the complex number in Cython, which uses the C99 standard of "complex.h" that has not been supported by the Visual Studio compiler.\n* it uses Cython to speed up the computationally expensive part (mainly the wavenumber integration).\n* The package has also provided three modes:\n  \n    * Serial mode: the serial version implements the FK algorithm in Python.\n    * Parallel mode on CPU: the wavenumber integration can be paralleled by MPI. \n    * Parallel mode on GPU: the wavenumber integration can also be paralleled by CUDA on GPU.\n\nInstallation\n-------------\n\nThe serial version and the parallel version on GPU can be simply installed using pip:\n\n.. code-block:: bash\n\n    pip install pyfk\n\nOr conda::\n\n    conda install -c ziyixi pyfk\n\nIt\'s also easy to install the MPI enabled version::\n\n    PYFK_USE_MPI=1 pip install pyfk[mpi]\n\nExtra packages including `numba <https://numba.readthedocs.io/en/stable/user/installing.html>`__ and `cupy <https://docs.cupy.dev/en/stable/install.html>`__ will be required to enable the GPU mode. For more details about the Installation, you can refer to the Installing part of the document.\n\nTodo\n------------------\nThe current bugs to fix or features to provide are listed in `TODO <https://github.com/ziyixi/pyfk/issues/5>`__.\n\nLicense\n-------\n\nPyFK is a free software: you can redistribute it and modify it under the terms of\nthe **Apache License**. A copy of this license is provided in\n`LICENSE <https://github.com/ziyixi/pyfk/blob/master/LICENSE>`__.\n',
    'author': 'Ziyi Xi',
    'author_email': 'xiziyi2015@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ziyixi/pyfk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.10',
}
from setup_cython import *
build(setup_kwargs)

setup(**setup_kwargs)
