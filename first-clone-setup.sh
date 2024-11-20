#!/usr/bin/env bash

set -e
set -o pipefail


#RDIR=$(git rev-parse --show-toplevel)

#git config --global protocol.file.allow always

RDIR=$(pwd)

cd $RDIR

echo "running build script"
# build setup
./build-setup.sh
source ~/.ssh/AGENT_VARS
echo "finished running build script"
cd sims/firesim
source sourceme-manager.sh --skip-ssh-setup

cd deploy
firesim managerinit --platform xilinx_alveo_u250
# copy config yml files
cp ../../../ae_config* .

# run through elaboration flow to get chisel/sbt all setup
#cd ../sim
#echo "chisel/sbt setup"
#make f1

cd $RDIR
# build target software
cd software/firemarshal
echo "Firemarshal setup"
./init-submodules.sh
./marshal -v build br-base.json
./marshal -v install br-base.json
echo "done marshal setup"

cd $RDIR
cd generators/ae-binary
unzip "*.zip"
cd ..
echo "supernova setup"
cd supernova/software
#submodule
git submodule update --init --recursive
#rm -rf imagenet
#unzip sample.zip
#rm sample.zip

echo "building workload"
# build workload
./build.sh
rm build/slam/*
#load sample binary
cp ../../ae-binary/*-linux build/slam/*


cd $RDIR
