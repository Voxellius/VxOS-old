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

        if ! git diff --name-only | grep src/$file && [ "$2" != "--force" ] && [ "$file" != "$2" ]; then
            continue
        fi

        echo "Uploading: src/$file -> $1/$file"
        mkdir -p $(dirname $file)
        cp $file $1/$file
    done
popd

echo "Upload complete!"