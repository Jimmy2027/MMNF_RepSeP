#!/usr/bin/env bash

python prepare.py || exit 1;
python train_models || exit 1;
