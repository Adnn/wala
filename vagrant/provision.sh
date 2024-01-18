#!/usr/bin/env bash

#
# Install required system packages
#
apt-get update
apt-get install -y python3-pip python3-venv nginx


#
# Install the wala application
#

# Put the venv out of the repository
VENV=.venv-wala
python3 -m venv ${VENV}
source ${VENV}/bin/activate

pushd /vagrant
pip3 install -e .
pip3 install gunicorn
popd

deactivate


#
# Server configuration
#

# Enable wala server in NGINX config
cp /vagrant/vagrant/wala.nginx /etc/nginx/sites-available/wala
pushd /etc/nginx/sites-enabled/
rm default
ln -s ../sites-available/wala .
popd
nginx -s reload

# Enable gunicorn service, auto starting
ln -s /vagrant/vagrant/gunicorn.service /etc/systemd/system/
sudo systemctl enable --now gunicorn.service
