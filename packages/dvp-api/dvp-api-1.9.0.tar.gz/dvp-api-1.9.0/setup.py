# Copyright (c) 2019, 2024 by Delphix. All rights reserved.

import setuptools

PYTHON_SRC = 'dvp-api'

install_requires = [
    'protobuf == 4.25.5'
]

with open('dvp-api/dlpx/virtualization/api/VERSION') as version_file:
    version = version_file.read().strip()

setuptools.setup(name='dvp-api',
                 version=version,
                 install_requires=install_requires,
                 package_dir={'': PYTHON_SRC},
                 packages=setuptools.find_packages(PYTHON_SRC),
                 include_package_data=True,
                 python_requires='==3.11.*',
                 )
