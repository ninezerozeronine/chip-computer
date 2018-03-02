#!/usr/bin/env bash

make clean
make html
rm -r ../docs/*
cp -a _build/html/. ../docs/
