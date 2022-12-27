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

convertFont titilliumweb-regular 16