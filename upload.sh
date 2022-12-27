#!/bin/bash

# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

shopt -s globstar dotglob

pushd src
    for file in **/*; do
        if git check-ignore $file -q; then
            continue
        fi

        if [ -d $file ]; then
            continue
        fi

        if ! git add --dry-run . | cut -d \' -f2 | grep src/$file && [ "$2" != "--force" ] && [ "$file" != "$2" ]; then
            continue
        fi

        echo "Uploading: src/$file -> $1/$file"
        mkdir -p $(dirname $1/$file)
        cp $file $1/$file
    done
popd

echo "Upload complete!"