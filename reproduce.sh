#!/usr/bin/env bash


python prepare_thesis/get_zenodo_data.py


./cleanup.sh || exit
./compile.sh thesis/thesis || exit
#./upload.sh || exit
echo "produce workflow finished"
