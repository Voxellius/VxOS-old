#!/bin/bash

# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

convertFont() {
    mkdir -p src/assets
    otf2bdf assets/$1.otf -o src/assets/$1-$2.bdf -p $2pt
}

pyftsubset assets/titilliumweb-regular.otf --output-file=assets/titilliumweb-numerals.otf --unicodes=U+0030-003A

convertFont titilliumweb-regular 16
convertFont titilliumweb-numerals 64