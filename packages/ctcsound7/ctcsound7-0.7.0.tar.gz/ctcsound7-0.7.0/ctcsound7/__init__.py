#   ctcsound7.py:
#
#   Wrapper around ctcsound.py to make it pip installable and version independent
#   This wrapper begins with compatibility with csound 6.18 and is usable also
#   with csound 7
#
#   Original copyright follows:
#
#   ctcsound.py:
#
#   Copyright (C) 2016 Francois Pinot§
#
#   This file is part of Csound.
#
#   This code is free software; you can redistribute it
#   and/or modify it under the terms of the GNU Lesser General Public
#   License as published by the Free Software Foundation; either
#   version 2.1 of the License, or (at your option) any later version.
#
#   Csound is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public
#   License along with Csound; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
#   02110-1301 USA
#

import ctypes as ct
import ctypes.util
import numpy as np
import sys
from . import _dll
from .common import MYFLT, string128, cstring, DEFMSGFUNC, BUILDING_DOCS

if not BUILDING_DOCS:
    libcsound, libcsoundPath = _dll.csoundDLL()
    VERSION = libcsound.csoundGetVersion()
    if VERSION >= 7000:
        APIVERSION = VERSION
    else:
        APIVERSION = libcsound.csoundGetAPIVersion()

    if VERSION < 7000:
        from .api6 import *
    else:
        from .api7 import *
else:
    print("------------- Building documentation -------------")
    VERSION = 0
    from . import api6
    from . import api7




#Instantiation
def csoundInitialize(flags):
    """Initializes Csound library with specific flags.

    This function is called internally by csoundCreate(), so there is generally
    no need to use it explicitly unless you need to avoid default initialization
    that sets signal handlers and atexit() callbacks.
    Return value is zero on success, positive if initialization was
    done already, and negative on error.
    """
    return libcsound.csoundInitialize(flags)


def setOpcodedir(s):
    """Sets an opcodedir override for csoundCreate()."""
    libcsound.csoundSetOpcodedir(cstring(s))


def setDefaultMessageCallback(function):
    """Not fully implemented. Do not use it yet except for disabling messaging:

    def noMessage(csound, attr, flags, *args):
        pass
    ctcsound.setDefaultMessageCallback(noMessage)
    """
    libcsound.csoundSetDefaultMessageCallback(DEFMSGFUNC(function))
