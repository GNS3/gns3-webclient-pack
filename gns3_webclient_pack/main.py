#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import os
import datetime
import locale
import signal

try:
    from gns3_webclient_pack.qt import QtCore, QtWidgets
except ImportError:
    raise SystemExit("Can't import Qt modules: Qt and/or PyQt is probably not installed correctly...")

from gns3_webclient_pack.main_window import MainWindow
from gns3_webclient_pack.application import Application
from gns3_webclient_pack.utils import parse_version
from gns3_webclient_pack.version import __version__

import logging
log = logging.getLogger(__name__)


def locale_check():
    """
    Checks if this application runs with a correct locale (i.e. supports UTF-8 encoding) and attempt to fix
    if this is not the case.

    This is to prevent UnicodeEncodeError with unicode paths when using standard library I/O operation
    methods (e.g. os.stat() or os.path.*) which rely on the system or user locale.

    More information can be found there: http://seasonofcode.com/posts/unicode-i-o-and-locales-in-python.html
    or there: http://robjwells.com/post/61198832297/get-your-us-ascii-out-of-my-face
    """

    # no need to check on Windows or when frozen
    if sys.platform.startswith("win") or hasattr(sys, "frozen"):
        return

    language = encoding = None
    try:
        language, encoding = locale.getlocale()
    except ValueError as e:
        log.error("could not determine the current locale: {}".format(e))
    if not language and not encoding:
        try:
            log.warning("could not find a default locale, switching to C.UTF-8...")
            locale.setlocale(locale.LC_ALL, ("C", "UTF-8"))
        except locale.Error as e:
            log.error("could not switch to the C.UTF-8 locale: {}".format(e))
            raise SystemExit
    elif encoding != "UTF-8":
        log.warning("your locale {}.{} encoding is not UTF-8, switching to the UTF-8 version...".format(language, encoding))
        try:
            locale.setlocale(locale.LC_ALL, (language, "UTF-8"))
        except locale.Error as e:
            log.error("could not set an UTF-8 encoding for the {} locale: {}".format(language, e))
            raise SystemExit
    else:
        log.info("current locale is {}.{}".format(language, encoding))


def checks():

    # Sometimes (for example at first launch) the OSX app service launcher add
    # an extra argument starting with -psn_. We filter it
    if sys.platform.startswith("darwin"):
        sys.argv = [a for a in sys.argv if not a.startswith("-psn_")]

    if hasattr(sys, "frozen"):
        # We add to the path where the OS search executable our binary location starting by GNS3
        # WebClient packaged binary
        frozen_dir = os.path.dirname(os.path.abspath(sys.executable))
        frozen_dirs = [frozen_dir]
        os.environ["PATH"] = os.pathsep.join(frozen_dirs) + os.pathsep + os.environ.get("PATH", "")

    # We only support Python 3 version >= 3.4
    if sys.version_info < (3, 4):
        raise SystemExit("Python 3.4 or higher is required")

    # We only support Qt version >= 5.6.0
    if parse_version(QtCore.QT_VERSION_STR) < parse_version("5.6.0"):
        raise SystemExit("Requirement is PyQt5 version 5.6.0 or higher, got version {}".format(QtCore.QT_VERSION_STR))

    # check for the correct locale (UNIX/Linux only)
    locale_check()

    try:
        os.getcwd()
    except FileNotFoundError:
        log.critical("The current working directory doesn't exist")
        return

    # always use the INI format on Windows and OSX (because we don't like the registry and plist files)
    if sys.platform.startswith('win') or sys.platform.startswith('darwin'):
        QtCore.QSettings.setDefaultFormat(QtCore.QSettings.IniFormat)


def main():
    """
    Entry point for GNS3 WebClient pack
    """

    checks()

    global app
    app = Application(sys.argv)

    current_year = datetime.date.today().year
    log.info("GNS3 WebClient pack version {}".format(__version__))
    log.info("Copyright (c) {} GNS3 Technologies Inc.".format(current_year))

    # We disallow to run GNS3 from outside the /Applications folder to avoid
    # issue when people run GNS3 from the .dmg
    if sys.platform.startswith("darwin") and hasattr(sys, "frozen"):
        if not os.path.realpath(sys.executable).startswith("/Applications"):
            error_message = "GNS3-webclient-pack.app must be moved to the '/Applications' folder before it can be used"
            QtWidgets.QMessageBox.critical(False, "Loading error", error_message)
            QtCore.QTimer.singleShot(0, app.quit)
            app.exec_()
            sys.exit(1)

    global mainwindow
    mainwindow = MainWindow()

    # Manage Ctrl + C or kill command
    def sigint_handler(*args):
        log.info("Signal received exiting the application")
        app.closeAllWindows()
    orig_sigint = signal.signal(signal.SIGINT, sigint_handler)
    orig_sigterm = signal.signal(signal.SIGTERM, sigint_handler)

    mainwindow.show()

    exit_code = app.exec_()
    signal.signal(signal.SIGINT, orig_sigint)
    signal.signal(signal.SIGTERM, orig_sigterm)

    delattr(MainWindow, "_instance")

    # We force deleting the app object otherwise it's segfault on Fedora
    del app
    # We force a full garbage collect before exit for unknown reason
    # otherwise Qt Segfault on OSX in some conditions
    import gc
    gc.collect()

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
