#!/usr/bin/env bash



# shellcheck disable=SC2164
pushd prepare_thesis
  ./prepare_thesis/run.sh || exit 1
popd

./cleanup.sh || exit
./compile.sh thesis/thesis || exit
#./upload.sh || exit
echo "produce workflow finished"
