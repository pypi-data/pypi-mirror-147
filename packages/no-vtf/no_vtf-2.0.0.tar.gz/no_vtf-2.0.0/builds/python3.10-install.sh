#!/bin/bash

# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: GPL-3.0-or-later

source builds/common

PREFIX='/usr/local'

cd "$(mktemp --directory)"
git clone --quiet --branch 3.10 --depth 1 'https://github.com/python/cpython.git' .

export LD_RUN_PATH="$PREFIX"'/lib'
./configure --prefix "$PREFIX" --enable-shared --with-lto >/dev/null
make --silent --jobs "$(nproc)"
sudo make altinstall >/dev/null

python3.10 --version
