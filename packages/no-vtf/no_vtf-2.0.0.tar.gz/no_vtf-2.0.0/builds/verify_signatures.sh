#!/bin/bash

# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: GPL-3.0-or-later

source builds/common

gpg --recv-keys 46C4ACD8B7B3F77DC8C2E8ED1C3724DFF9CEAF64  # b5327157@protonmail.com

git rev-list --all | chronic xargs --no-run-if-empty git verify-commit
git tag --list | chronic xargs --no-run-if-empty git verify-tag
