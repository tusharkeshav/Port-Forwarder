from log.Logging import log
import os
import configparser as cp

HOME = os.environ['HOME']  # Note: This is only for Linux distributions

config = cp.ConfigParser()

# Note: Below optionxform is added coz ConfigParser was turning All Uppercase config key to lowercase automatically.
# https://stackoverflow.com/q/19359556/9730403

config.optionxform = str
config.read('properties/config.ini')


def set_property(prop, value: str):
    value = value.replace("'", "\"")
    config.set('PROPERTIES', prop, value)
    log.debug('Setting property in config file. prop: {prop}, value: {value}'.format(prop=prop, value=value))
    with open('properties/config.ini', 'w') as configfile:
        config.write(configfile)
        configfile.close()


def set_ngrok_secret(secret: str):
    set_property(prop='NGROK_API_SECRET', value=secret)
    tmp = secret[:3] + ('X'* (len(secret)-6)) + secret[-3:]
    log.info('Config.ini is updated with new ngrok secret: {}'.format(tmp))


def set_cutt_ly_secret(secret: str):
    set_property(prop='CUTTLY_SECRET', value=secret)
    log.info('config.ini is updated with new cuttly secret')


def set_alias(alias: str):
    set_property(prop='ALIAS', value=alias)
    log.info('config.ini is updated with new alias: {}'.format(alias))


def set_port_protocol(port, protocol):
    set_property(prop='PROTOCOL_PORT', value="{p}".format(p=list((protocol, port))))
    log.info('config.ini is updated with new port and protocol: {}'.format(list((protocol, port))))


def set_ngrok_auth_token(auth_token):
    ngrok_yaml_file = 'version: 2 \nauthtoken: {auth_token} \nconsole_ui: false'.format(auth_token=auth_token)
    path = HOME + '/.config/ngrok/'
    filename = 'ngrok.yml'
    os.makedirs(path, exist_ok=True)
    full_path = path + filename
    with open(full_path, 'w+') as file:
        file.write(ngrok_yaml_file)
        file.close()
    tmp = auth_token[:3] + 'X' * len(auth_token) + auth_token[-3:]
    log.info('Modified ngrok auth-token with new token: {}'.format(tmp))
