import json

class Config(object):
    with open('config.conf','r') as f:
        data = json.load(f)
    DATABASE = data['Database']
    SECRET_KEY = data['Secret_Key']