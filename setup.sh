cd ~
mkdir ddns
mkdir -p ~/.config/systemd/user
cd ddns
git clone placeholder .
# on host please run this (at project directory) after clone: scp .env nduc@server.home:~/ddns/.env
echo "On host please run this ssh command (at project directory) after clone: scp .env nduc@server.home:~/ddns/.env."
read -p "Press enter to continue after .env file is copied"
pip install -r requirements.txt
cp ddns.service ~/.config/systemd/user/ddns.service
systemctl --user daemon-reload
systemctl --user enable ddns.service