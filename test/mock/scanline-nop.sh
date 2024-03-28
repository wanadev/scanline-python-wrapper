#!/bin/bash

DIR_NAME="."
FILE_NAME="scan"
FILE_EXT=".pdf"

while [ ! -z "$1" ] ; do
    case "$1" in
        "-dir")
            DIR_NAME="$2"
            ;;
        "-name")
            FILE_NAME="$2"
            ;;
        "-tiff")
            FILE_EXT=".tif"
            ;;
        "-jpeg")
            FILE_EXT=".jpg"
            ;;
    esac
    shift
done

touch "${DIR_NAME}/${FILE_NAME}${FILE_EXT}"

exit 0
