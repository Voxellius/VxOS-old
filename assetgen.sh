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

convertImage() {
    mkdir -p src/assets
    convert assets/$1.png -depth 1 src/assets/$1.bmp
}

convertImageSmall() {
    mkdir -p src/assets
    convert assets/$1.png -dither none -colors 2 -remap assets/palette.png -compress none -type palette BMP3:src/assets/$1.bmp
}

pyftsubset assets/titilliumweb-regular.otf --output-file=assets/titilliumweb-numerals.otf --unicodes=U+0030-003A

convertFont titilliumweb-regular 16
convertFont titilliumweb-numerals 64

convertImageSmall boot
convertImage battery-0
convertImage battery-1
convertImage battery-2
convertImage battery-3
convertImage battery-4
convertImage battery-5
convertImage battery-6
convertImage battery-7
convertImage battery-8
convertImage battery-9
convertImage battery-10
convertImage appicon