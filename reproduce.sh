#!/usr/bin/env bash


python prepare_thesis/get_zenodo_data.py

find data/ -name ".DS_Store" -delete || exit 1

./cleanup.sh || exit
./compile.sh thesis/thesis || exit
#./upload.sh || exit
echo "produce workflow finished"
