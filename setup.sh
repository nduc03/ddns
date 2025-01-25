echo "Ask for sudo password..."
sudo echo "Done."
cd ~
mkdir ddns
cd ddns
git clone https://github.com/nduc03/ddns.git .
# on host please run this (at project directory) after clone: scp .env nduc@server.home:~/ddns/.env
echo "On host please run this ssh command (at project directory) after clone: scp .env nduc@server.home:~/ddns/.env."
read -p "Press enter to continue after .env file is copied"
sudo pip install -r requirements.txt
sudo cp ddns.service etc/systemd/system/ddns.service
sudo systemctl daemon-reload
sudo systemctl --user enable ddns.service