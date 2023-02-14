# Po-Fo
![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)  ![GitHub](https://img.shields.io/badge/license-Apache-blue?style=popout-square) [![Awesome](https://awesome.re/badge-flat.svg)](https://awesome.re)
[![contributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/tusharkeshav/Port-Forwarder)

Dynamic Ngrok is a command line interface that ensure your port forwarding will up and work without an issue.
* It ensure that ngrok generated url always pointed to your custom alias.
* It ensure that it will recover from any intermittent failures like connectivity issues.
* It ensure reliability of system.
* Lot of service can be build on top of this.

# How it works?
It exposes the ngrok public url to a static custom short URL.
So, when the ngrok backend URL changes, it's the responsbility of service to correctly change/modify shorturl to new public url.
You have one custom url, now there's no need to get ngrok url. Service will automatically ensure that correct mapping between ngrok public url and short url exist.
Service uses cuttly url shortening service.

# System Structure
![image](https://user-images.githubusercontent.com/43966061/213911128-f4a1bb7c-79ca-4543-85cc-46f24cf846a1.png)

# Use Case:
- Can be used to reliably host server in raspberry pie.
- Can be used to build automation on top of it.
- Can be used to transfer file using SSH or stfp.
- Host a server. No need to rely for costly servers(if yor doing it for temporary purposes)

## First time installation:
* [Set up ngrok auth-token manually](https://github.com/tusharkeshav/Port-Forwarder/wiki/Setting-ngrok-auth-token). It can be done using `python3 main.py --ngrok_auth_token <auth-token>`
* [Get api key from cut.ly](https://github.com/tusharkeshav/Port-Forwarder/wiki/Setting-up-Cutt.ly-API)
* [Generate Ngrok API secret](https://github.com/tusharkeshav/Port-Forwarder/wiki/Generating-Ngrok-API-Key)
> __Note__: NGROK API secret is different from NGROK AUTH-TOKEN. NGROK API secret is use to authenticate api and NGROK auth-token is used to access establish a successful tunnel/port forwarding on behealf of particular user account.

## Configurations: (path: /properties/config.ini)
> __Note__: Ensure all config properties are in place before running the script.
```
NGROK_API_SECRET = <NGROK API SECRET>
NGROK_TUNNEL_ENDPOINT = https://api.ngrok.com/tunnels # it's tunnel
CUTTLY_SECRET = <CUTTLY API SECRET>
CUTTLY_API_ENDPOINT = http://cutt.ly/api/api.php
CUTTLY_DOMAIN = https://cutt.ly/
ALIAS = test123  # <Custom alias: it will look like -> https://cutt.ly/test123>
BINARY_PATH = ./ngrok
PROTOCOL_PORT = ["http","456"] # set your protocol and port you want to forward. Protocol is always tcp or http.
```

## Installation:
```
git clone https://github.com/tusharkeshav/Port-Forwarder.git
pip3 install -r requirements.txt
python3 main.py
```

## Docker:
It can be run in docker.
```
sudo docker build --tag portforwarder .  # create an image
sudo docker run -it portforwarder        # run in interactive mode
sudo docker run exec <container-name or container-id> tail -50f /app/log/Application.log  # To view logs
```

## FAQ
- [How to use](https://github.com/tusharkeshav/Port-Forwarder/wiki/How-to-use) </br>
- [Passing Config via Arguments](https://github.com/tusharkeshav/Port-Forwarder/wiki/Passing-config-via-args:) </br>
We have provided ngrok binary with this as well. It's same binary provided by ngrok. You can verify via checksum.
Follow wiki for more.
