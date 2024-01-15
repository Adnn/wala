#!/usr/bin/env bash
apt-get update
apt-get install -y python3-pip python3-venv nginx

# Put the venv out of the repository
VENV=.venv-vagrant
python3 -m venv ${VENV}
source ${VENV}/bin/activate

pushd /vagrant
pip3 install -r requirements.txt
