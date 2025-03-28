#!/bin/bash
# veyon-setup-teacher for setup Veyon configurator for teacher host.
# Create by Kittirak Moungmingsuk <kittirak@yahoo.com> and chatgpt
# Last modify: 14 Sep 2024

# Need to set only one below variable (VEYON_URL)
VEYON_URL=https://github.com/veyon/veyon/releases/download/v4.8.3/veyon_4.8.3.0-ubuntu.focal_amd64.deb

VEYON_FILENAME=`basename ${VEYON_URL}`

# 0. Install com2kids.deb
echo "Install com2kids.deb"
sudo dpkg -i com2kids/deb/com2kids.deb

# 1. Install veyon depends
sudo apt -y install libfakekey0 libqca-qt5-2 

# 2. Download and install veyon
echo "install ${VEYON_FILENAME}"
if [ ! -f ${HOME}/Downloads/${VEYON_FILENAME} ]; then
  wget -O ${HOME}/Downloads/${VEYON_FILENAME} ${VEYON_URL}
fi

sudo dpkg -i ${HOME}/Downloads/${VEYON_FILENAME} 

# 3. create com2kids key pair to directory 
sudo veyon-cli authkeys create com2kids

# set authentication method to key
sudo veyon-cli config set Authentication/Method 1

# 3.1 create location
veyon-cli networkobjects add location "Computer Room"

# 4. install server app python requirement
sudo apt install -y python3-pip

# install requirements
echo "Install python require packages"
pip install fastapi uvicorn uvloop httptools==0.1.2
sudo apt install -y uvicorn

# 5. set FQDN
read -p "Please specify FQDN :" FQDN
echo "hostnamectl set-hostname ${FQDN}"
hostnamectl set-hostname ${FQDN}

# 6. run server
echo "start server.py"
cd com2kids
uvicorn server:app --host 0.0.0.0 --port 8000
