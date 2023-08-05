# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

import multiprocessing

from no_vtf.main import main

if __name__ == "__main__":
    multiprocessing.freeze_support()

    main()
