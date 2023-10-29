#!/usr/bin/env python
#
# Copyright (C) 2023 GNS3 Technologies Inc.
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
import shutil
import subprocess

from pathlib import Path
from gns3_webclient_pack.qt import QtCore
from gns3_webclient_pack.utils.get_resource import get_resource

try:
    import importlib_resources
except ImportError:
    from importlib import resources as importlib_resources


def install_mime_types():

    if not sys.platform.startswith("linux"):
        raise SystemExit("Installing mime types is only possible on Linux")

    applications_location = Path(QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.ApplicationsLocation))
    generic_data_location = Path(QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.GenericDataLocation))

    try:
        # install the gns3-webclient-config.desktop file
        applications_location.mkdir(parents=True, exist_ok=True)
        desktop_file = get_resource("linux/applications/gns3-webclient-config.desktop")
        desktop_dst_path = applications_location / "gns3-webclient-config.desktop"
        if not desktop_dst_path.exists():
            print(f"Installing {desktop_file} resource file to {desktop_dst_path}")
            shutil.copy(desktop_file, desktop_dst_path)
        else:
            print(f"Skipping {desktop_file} resource file (already installed)")

        # install the gns3-webclient-launcher.desktop file
        desktop_file = get_resource("linux/applications/gns3-webclient-launcher.desktop")
        desktop_dst_path = applications_location / "gns3-webclient-launcher.desktop"
        if not desktop_dst_path.exists():
            print(f"Installing {desktop_file} resource file to {desktop_dst_path}")
            shutil.copy(desktop_file, desktop_dst_path)
        else:
            print(f"Skipping {desktop_file} resource file (already installed)")

        # install the icons
        icons_directory = generic_data_location / "icons"
        icons_directory.mkdir(parents=True, exist_ok=True)

        def install_icons(resource, directory):
            for entry in importlib_resources.files(resource).iterdir():
                dst_path = directory / entry.name
                if entry.is_file():
                    if not dst_path.exists():
                        print(f'Installing {entry} resource file to "{dst_path}"')
                        shutil.copy(str(entry), dst_path)
                    else:
                        print(f"Skipping {entry} resource file (already installed)")
                if entry.is_dir():
                    dst_path.mkdir(parents=True, exist_ok=True)
                    install_icons(f"{resource}.{entry.name}", dst_path)

        install_icons('gns3_webclient_pack.linux.icons', icons_directory)

    except OSError as e:
        raise SystemExit("Could not install mime types: {}".format(e))

    try:
        # update the MIME and application databases
        subprocess.run(["update-mime-database", str(generic_data_location / "mime")], check=True)
        subprocess.run(["update-desktop-database", str(applications_location)], check=True)
        print("MIME and application databases updated")
    except OSError as e:
        raise SystemExit("Could not update MIME and application databases: {}".format(e))
