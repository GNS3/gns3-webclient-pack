# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 GNS3 Technologies Inc.
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
import os
import subprocess

from setuptools import setup, find_packages
from gns3_webclient_pack.version import __version__

# we only support Python 3 version >= 3.4
if len(sys.argv) >= 2 and sys.argv[1] == "install" and sys.version_info < (3, 4):
    raise SystemExit("Python 3.4 or higher is required")

if sys.platform.startswith("linux"):
    data_files = [
        ("share/applications", ["resources/linux/applications/gns3-webclient-launcher.desktop",
                                "resources/linux/applications/gns3-webclient-config.desktop"]),
        ("share/icons/hicolor/16x16/apps", ["resources/linux/icons/hicolor/16x16/apps/gns3_webclient.png"]),
        ("share/icons/hicolor/32x32/apps", ["resources/linux/icons/hicolor/32x32/apps/gns3_webclient.png"]),
        ("share/icons/hicolor/48x48/apps", ["resources/linux/icons/hicolor/48x48/apps/gns3_webclient.png"]),
        ("share/icons/hicolor/scalable/apps", ["resources/linux/icons/hicolor/scalable/apps/gns3_webclient.svg"]),
    ]
else:
    data_files = []

dependencies = open("requirements.txt", "r").read().splitlines()

dist = setup(
        name="gns3-webclient-pack",
        version=__version__,
        url="http://github.com/GNS3/gns3-client-pack",
        license="GNU General Public License v3 (GPLv3)",
        author="Jeremy Grossmann",
        author_email="developers@gns3.net",
        description="GNS3 WebClient pack to use with the GNS3 web interface",
        long_description=open("README.md", "r").read(),
        long_description_content_type="text/markdown",
        install_requires=dependencies,
        entry_points={
            "gui_scripts": [
                "gns3-webclient-config = gns3_webclient_pack.main:main",
                "gns3-webclient-launcher = gns3_webclient_pack.launcher:main"
            ]
        },
        data_files=data_files,
        packages=find_packages(".", exclude=["docs", "tests"]),
        platforms="any",
        classifiers=[
            "Development Status :: 4 - Beta",
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
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: Implementation :: CPython",
        ],
)

if sys.platform.startswith("linux") and os.geteuid() == 0 and dist is not None:

    # update the XDG .desktop file database
    try:
        sys.stdout.write('Updating the XDG .desktop file database.\n')
        subprocess.call(["update-desktop-database", "-q"])
    except:
        sys.stderr.write("Could not update the XDG .desktop file database")

    # update the shared MIME-Info database cache
    try:
        sys.stdout.write('Updating the shared MIME-Info database cache.\n')
        subprocess.call(["update-mime-database", "-n", os.path.join(sys.prefix, "share/mime/")])
    except:
        sys.stderr.write("Could not update shared MIME-Info database cache")
else:
    print("Could not update the XDG .desktop file and shared MIME-Info databases")
