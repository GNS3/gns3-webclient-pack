#!/usr/bin/env python
#
# Copyright (C) 2019 GNS3 Technologies Inc.
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

import re


def parse_version(version):
    """
    Return a comparable tuple from a version string. We try to force tuple to semver with version like 1.2.0

    Replace pkg_resources.parse_version which now display a warning when use for comparing version with tuple

    :returns: Version string as comparable tuple
    """

    release_type_found = False
    version_infos = re.split(r'(\.|[a-z]+)', version)
    version = []
    for info in version_infos:
        if info == '.' or len(info) == 0:
            continue
        try:
            info = int(info)
            # We pad with zero to compare only on string
            # This avoid issue when comparing version with different length
            version.append("%06d" % (info,))
        except ValueError:
            # Force to a version with three number
            if len(version) == 1:
                version.append("00000")
            if len(version) == 2:
                version.append("000000")
            # We want rc to be at lower level than dev version
            if info == 'rc':
                info = 'c'
            version.append(info)
            release_type_found = True
    if release_type_found is False:
        # Force to a version with three number
        if len(version) == 1:
            version.append("00000")
        if len(version) == 2:
            version.append("000000")
        version.append("final")
    return tuple(version)
