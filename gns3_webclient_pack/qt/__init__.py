# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 GNS3 Technologies Inc.
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

"""
Compatibility layer for Qt bindings, so it is easier to switch to PySide if needed.
"""

# based on https://gist.github.com/remram44/5985681 and
# https://github.com/pyQode/pyqode.qt/blob/master/pyqode/qt/QtWidgets.py (MIT license)


import sys
import inspect
import functools

try:
    from PyQt5 import sip
except ImportError:
    import sip

from PyQt5 import QtCore, QtGui, QtNetwork, QtWidgets
sys.modules[__name__ + '.QtCore'] = QtCore
sys.modules[__name__ + '.QtGui'] = QtGui
sys.modules[__name__ + '.QtNetwork'] = QtNetwork
sys.modules[__name__ + '.QtWidgets'] = QtWidgets
sys.modules[__name__ + '.sip'] = sip

QtCore.Signal = QtCore.pyqtSignal
QtCore.Slot = QtCore.pyqtSlot
QtCore.Property = QtCore.pyqtProperty


def sip_is_deleted(obj):
    """
    :return: True if object no longer exists
    """
    if obj is None or (isinstance(obj, sip.simplewrapper) and sip.isdeleted(obj)):
        return True
    return False


def qpartial(func, *args, **kwargs):
    """
    A functools partial that you can use on QObject. the partial is not called
    if the targeted QObject is destroyed .
    """

    if func is None:
        return None

    if inspect.ismethod(func):
        if isinstance(func.__self__, QtCore.QObject):

            def partial(*args, **kwargs):
                if sip_is_deleted(func.__self__):
                    return
                return func(*args, **kwargs)
            return functools.partial(partial, *args, **kwargs)

    return functools.partial(func, *args, **kwargs)
