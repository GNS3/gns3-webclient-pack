# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from setuptools import setup, find_packages

# we only support Python 3 version >= 3.4
if len(sys.argv) >= 2 and sys.argv[1] == "install" and sys.version_info < (3, 4):
    raise SystemExit("Python 3.4 or higher is required")

setup(
    name="gns3-client-pack",
    version=__import__("gns3_webclient_pack").__version__,
    url="http://github.com/GNS3/gns3-client-pack",
    license="GNU General Public License v3 (GPLv3)",
    author="Jeremy Grossmann",
    author_email="developers@gns3.net",
    description="GNS3 client pack to use with the GNS3 web interface",
    long_description=open("README.rst", "r").read(),
    install_requires=open("requirements.txt", "r").read().splitlines(),
    entry_points={
        "gui_scripts": [
            "gns3-webclient-config = gns3_webclient_pack.main:main"
            "gns3-webclient-launcher = gns3_webclient_pack.launcher:main"
        ]
    },
    packages=find_packages(".", exclude=["docs", "tests"]),
    include_package_data=True,
    platforms="any",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: Information Technology",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
