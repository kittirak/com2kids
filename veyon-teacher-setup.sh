#!/bin/bash
# veyon-setup-teacher for setup Veyon configurator for teacher host.
# Create by Kittirak Moungmingsuk <kittirak@yahoo.com> and chatgpt
# Last modify: 14 Sep 2024

# Need to set only one below variable (VEYON_URL)
VEYON_URL=https://github.com/veyon/veyon/releases/download/v4.8.3/veyon_4.8.3.0-ubuntu.focal_amd64.deb

VEYON_FILENAME=`basename ${VEYON_URL}`

# 0. Install com2kids.deb
echo "Install com2kids.deb"
wget https://github.com/kittirak/com2kids/deb/com2kids.deb
sudo dpkg -i com2kids.deb

# 1. Install veyon depends
sudo apt -y install libfakekey0 libqca-qt5-2 

# 2. Download and install veyon
echo "install ${VEYON_FILENAME}"
if [ ! -f /home/com2kids/Downloads/${VEYON_FILENAME} ]; then
  wget -O /home/com2kids/Downloads/${VEYON_FILENAME} ${VEYON_URL}
fi

sudo dpkg -i /home/com2kids/Downloads/${VEYON_FILENAME} 

# 3. create com2kids key pair to directory 
sudo veyon-cli authkeys create com2kids

# set authentication method to key
sudo veyon-cli config set Authentication/Method 1

# 4. install server app python requirement
sudo apt install -y python3-pip

# install requirements
pip install fastapi uvicorn uvloop httptools==0.1.2

echo "wget https://github.com/kittirak/com2kids/server.py"

# 5. set FQDN
read -p "Please specify FQDN :" FQDN
echo "hostnamectl set-hostname ${FQDN}"
hostnamectl set-hostname ${FQDN}

# 6. run server
uvicorn server:app --host 0.0.0.0 --port 8000
