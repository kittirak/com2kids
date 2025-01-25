#!/bin/sh

if [ -z "$1" ] ; then
  echo "Please specific teacher hostname or IP"
  echo "Usage: $0 [IP]"
  exit 1
fi

# 1. Install veyon (download from teacher host)

# install depends
sudo apt -y install libfakekey0 libqca-qt5-2 

echo "curl -OJ http://${1}:8000/download/veyon"
VEYON_FILENAME=$(curl -OJ http://${1}:8000/download/veyon 2>&1 | grep -oP "(?<=Saved to filename ').*(?=')")
mv ${VEYON_FILENAME} /home/com2kids/Downloads
echo "Install Veyon (${VEYON_FILENAME})"
sudo dpkg -i /home/com2kids/Downloads/${VEYON_FILENAME}

# 2. Set public key (retrive from teacher host)
sudo mkdir -p /etc/veyon/keys/public/com2kids
curl http://${1}:8000/keys/public | python3 -c "import sys, json; print(json.load(sys.stdin)['public_key'])" > key
sudo mv key /etc/veyon/keys/public/com2kids/key  
sudo chmod 444 /etc/veyon/keys/public/com2kids/key

# set authentication method to key
sudo veyon-cli config set Authentication/Method 1

# 3. start veyon service
sudo systemctl start veyon

# 4. Register client to server(teacher)
# grep IP 
IP=$(hostname -I | awk '{print $1}')

# send IP to server(teacher host) and receive hostname 
NEW_HOSTNAME=`curl -X POST "http://${1}:8000/client/config" -H "Content-Type: application/json" -d '{"ip": "'$IP'"}' | \
    python3 -c "import sys, json; print(json.load(sys.stdin)['new_hostname'])"`

# 5. Set hostname (essentail for usage statistics)
echo "Set hostname (FQDN) $NEW_HOSTNAME"
sudo hostnamectl set-hostname $NEW_HOSTNAME
