#!/usr/bin/env bash

mkdir -p build
cp -r src/* build/
cd build
for dir in *
do
    bdbag --update --archive zip "$dir"
done

