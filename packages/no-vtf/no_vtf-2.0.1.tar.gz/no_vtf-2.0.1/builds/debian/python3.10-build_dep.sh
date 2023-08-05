#!/bin/bash

# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: GPL-3.0-or-later

source builds/common

echo 'deb-src http://deb.debian.org/debian stable main' |
	sudo tee --append /etc/apt/sources.list >/dev/null
sudo apt-get update
sudo apt-get build-dep python3.9
# The control file of python3.9 contains "Build-Conflicts: git" to prevent "encoding git
# information of the packaging in the upstream version information", here it is useful.
sudo apt-get install git
