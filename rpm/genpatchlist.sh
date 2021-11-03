#!/bin/sh
num=0
# Order patches with zeros in front so rpm applies the patches in the specified order
zeros=000

while read -r patch ; do
    if grep -q 'Debian-specific' rpm/patches/debian/$patch ; then
        # Filter out Debian specific patches
        continue
    fi
    echo Patch${zeros}${num}: patches/debian/"$patch"
    export num=$((num+1))
    if [ $((num/100)) -eq 1 ] ; then
        zeros=0
    elif [ $((num/10)) -eq 1 ] ; then
        zeros=00
    fi

    # read patching order from debian quilt file
done < rpm/patches/debian/series

find rpm/patches  -maxdepth 1  -name \*.patch -printf %P\\n | sort | while read -r patch ; do
    echo Patch${zeros}${num}: patches/"$patch"
    export num=$((num+1))

    if [ $((num/100)) -eq 1 ] ; then
        zeros=0
    elif [ $((num/10)) -eq 1 ] ; then
        zeros=00
    fi
done
