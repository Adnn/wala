#!/usr/bin/env bash

#
# Install required system packages
#
apt-get update
apt-get install -y python3-pip python3-venv nginx


#
# Install the wolo application
#

# Put the venv out of the repository
VENV=.venv-wolo
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

# Enable wolo server in NGINX config
cp /vagrant/vagrant/wolo.nginx /etc/nginx/sites-available/wolo
pushd /etc/nginx/sites-enabled/
rm default
ln -s ../sites-available/wolo .
popd
nginx -s reload

# Enable gunicorn service, auto starting
ln -s /vagrant/vagrant/gunicorn.service /etc/systemd/system/
sudo systemctl enable --now gunicorn.service
