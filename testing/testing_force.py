import requests
import sys
sys.path.append(r'../config')
sys.path.append(r'../action')
sys.path.append(r'../server')
import time
from config.mischbares_small import config
import json
from copy import copy

def force_test(action, params):
    server = 'forceAction'
    action = action
    params = params
    res = requests.get("http://{}:{}/{}/{}".format(
        config['servers']['sensingServer']['host'], 
        config['servers']['sensingServer']['port'],server , action),
        params= params).json()
    return res

force_test('read', None)
