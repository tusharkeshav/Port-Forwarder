import configparser as cp
import json

config = cp.ConfigParser()
config.read('properties/config.ini')
ngrok_secret = config.get('PROPERTIES', 'NGROK_API_SECRET')
BASE_TUNNEL_URL = config.get('PROPERTIES', 'NGROK_TUNNEL_ENDPOINT')

cutt_ly_secret = config.get('PROPERTIES', 'CUTTLY_SECRET')
BASE_API_URL = config.get('PROPERTIES', 'CUTTLY_API_ENDPOINT')
BASE_DOMAIN = config.get('PROPERTIES', 'CUTTLY_DOMAIN')

SSH_custom_alias = config.get('PROPERTIES', 'ALIAS')  # it will be like https://cutt.ly/testxyz12
binary_path = config.get('PROPERTIES', 'BINARY_PATH')
PORT = json.loads(config.get('PROPERTIES', 'PROTOCOL_PORT'))  # port to be forwarded
