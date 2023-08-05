#!/bin/bash

# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: GPL-3.0-or-later

source builds/common

[ -n "$1" ]

cd "$(mktemp --directory)"
git clone --quiet --no-checkout "$OLDPWD" .
git checkout --quiet HEAD

exec "$@"
