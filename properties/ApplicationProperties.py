import configparser as cp
import json
from log.Logging import log

config = cp.ConfigParser()
# Note: Below optionxform is added coz ConfigParser was turning All Uppercase config key to lowercase automatically.
# https://stackoverflow.com/q/19359556/9730403
config.optionxform = str


def NGROK_SECRET():
    config.read('properties/config.ini')
    return config.get('PROPERTIES', 'NGROK_API_SECRET')


def BASE_TUNNEL_URL():
    config.read('properties/config.ini')
    return config.get('PROPERTIES', 'NGROK_TUNNEL_ENDPOINT')


def CUTTLY_SECRET():
    config.read('properties/config.ini')
    return config.get('PROPERTIES', 'CUTTLY_SECRET')


def BASE_API_URL():
    config.read('properties/config.ini')
    return config.get('PROPERTIES', 'CUTTLY_API_ENDPOINT')


def BASE_DOMAIN():
    config.read('properties/config.ini')
    return config.get('PROPERTIES', 'CUTTLY_DOMAIN')


def SSH_CUSTOM_ALIAS():
    config.read('properties/config.ini')
    return config.get('PROPERTIES', 'ALIAS')


def BINARY_PATH():
    config.read('properties/config.ini')
    return config.get('PROPERTIES', 'BINARY_PATH')


def PORT():
    config.read('properties/config.ini')
    return json.loads(config.get('PROPERTIES', 'PROTOCOL_PORT'))


def set_property(prop, value: str):
    config.read('properties/config.ini')
    value = value.replace("'", "\"")
    config.set('PROPERTIES', prop, value)
    log.debug('Setting property in config file. prop: {prop}, value: {value}'.format(prop=prop, value=value))
    with open('properties/config.ini', 'w') as configfile:
        config.write(configfile)
        configfile.close()
