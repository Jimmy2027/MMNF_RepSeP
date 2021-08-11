#!/usr/bin/env bash


python prepare/run.py


./cleanup.sh || exit
./compile.sh midterm_presentation/midterm_slides || exit
#./upload.sh || exit
echo "produce workflow finished"
