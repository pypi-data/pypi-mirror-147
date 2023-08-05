# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    try:
        from no_vtf._version import version as __version__
    except ImportError:
        __version__ = "UNKNOWN"
else:
    __version__ = "TYPE_CHECKING"
