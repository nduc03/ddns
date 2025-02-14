## How to setup Cloudflare DDNS
1. Open ssh
    ```sh
    ssh nduc@server.lan
    ```

2. Setting up needed files
    ```sh
    cd ~
    mkdir ddns
    cd ddns
    git clone https://github.com/nduc03/ddns.git .
    ```

3. Run this on local machine (at project directory) outside the ssh session above after clone:
    ```sh
    scp .env nduc@server.lan:~/ddns/.env
    ```

4. After .env file is copied, run these commands to start the service:
    ```sh
    sudo apt install python3-requests
    sudo cp ddns.service /etc/systemd/system/cloudflare-ddns.service
    sudo systemctl daemon-reload
    sudo systemctl enable cloudflare-ddns
    sudo systemctl start cloudflare-ddns
    ```

## How to update service
1. Open ssh and pull new code:
    ```sh
    cd ~/ddns
    git pull
    ```
2. If .env is modified, run this on local machine (at project directory) outside the ssh session:
    ```sh
    scp .env nduc@server.lan:~/ddns/.env
    ```
3. Restart service:
    ```sh
    sudo systemctl restart cloudflare-ddns
    ```
