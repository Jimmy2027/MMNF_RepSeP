#!/usr/bin/env bash


python prepare/plot_model_examples.py


./cleanup.sh || exit
./compile.sh || exit
#./upload.sh || exit
echo "produce workflow finished"
