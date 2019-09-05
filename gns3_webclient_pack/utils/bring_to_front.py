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

import sys
import logging
log = logging.getLogger(__name__)


def get_windows_from_pid(pid):

    import win32process
    import win32gui

    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds


def set_foreground_window(hwnd):

    import pywintypes
    import win32gui
    import win32con

    try:
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        if win32gui.IsWindowVisible(hwnd) == 0:
            win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        win32gui.SetForegroundWindow(hwnd)
    except pywintypes.error as e:
        log.debug("Could not bring window to front '{}'".format(e.strerror))


def bring_window_to_front_from_pid(pid):

    assert sys.platform.startswith("win") is True
    for hwnd in get_windows_from_pid(pid):
        set_foreground_window(hwnd)
