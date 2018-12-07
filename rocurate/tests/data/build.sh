#!/usr/bin/env bash

rm -r build
mkdir build
cp -r src/* build/
cd build
for dir in *
do
    bdbag --update --archive zip $dir
done

