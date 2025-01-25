## How to setup Cloudflare DDNS
1. Open ssh
    ```sh
    ssh nduc@server.home
    ```

2. Setting up needed files
    ```sh
    cd ~
    mkdir ddns
    cd ddns
    git clone https://github.com/nduc03/ddns.git .
    ```

3. Run this on host (at project directory) and outside the ssh session above after clone:
    ```sh
    scp .env nduc@server.home:~/ddns/.env
    ```

4. After .env file is copied, run these commands to start the service:
    ```sh
    sudo apt install python3-requests
    sudo cp ddns.service /etc/systemd/system/ddns.service
    sudo systemctl daemon-reload
    sudo systemctl enable ddns.service
    sudo systemctl start ddns.service
    ```