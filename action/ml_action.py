import sys
sys.path.append(r'../driver')
sys.path.append(r'../action')
sys.path.append(r'../config')
#from mischbares_small import config

from celery import group
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import json
import requests
import pickle
import os
from importlib import import_module
helao_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(helao_root)
sys.path.append(os.path.join(helao_root, 'config'))
config = import_module(sys.argv[1]).config
from ml_driver import DataUtilSim

app = FastAPI(title="analysis action server",
              description="This is a test measure action",
              version="1.0")


class return_class(BaseModel):
    parameters: dict = None
    data: dict = None


@app.get("/learning/gaus_model")
def gaus_model(length_scale: int = 1, restart_optimizer: int = 10, random_state: int = 42):
    model = d.gaus_model(length_scale, restart_optimizer, random_state)
    retc = return_class(parameters={'length_scale': length_scale, 'restart_optimizer': restart_optimizer, 'random_state': random_state}, data={
                        'model': model})
    return retc

# we still need to discuss about the data type that we are adding here.


@app.get("/learning/activeLearning")
def active_learning_random_forest_simulation(sources: str, x_query: str, save_data_path: str = 'ml_data/ml_analysis.json', addresses: str = "schwefel_function/data/key_y"):
    """
    if sources == "session":
        sources = requests.get("http://{}:{}/{}/{}".format(config['servers']['orchestrator']['host'], 
                config['servers']['orchestrator']['port'], 'orchestrator', 'getSession'), params=None).json()
    else:
        try:
            sources = json.loads(sources)
            if "session" in sources:
                sources[sources.index("session")] = requests.get("http://{}:{}/{}/{}".format(config['servers']['orchestrator']['host'], 
                config['servers']['orchestrator']['port'], 'orchestrator', 'getSession'), params=None).json()
        except:
            pass
    """  
    print("i am in learning")
    with open('C:/Users/LaborRatte23-3/Documents/session/sessionLearning.pck', 'rb') as banana:
        sources = pickle.load(banana)  
    print(sources)
    

    print("I am learning.")
    next_exp_dx, next_exp_dy, next_exp_pos  = d.active_learning_random_forest_simulation(
        sources, x_query, save_data_path, addresses)

    # next_exp_pos : would be a [dx, dy] of the next move
    # prediction : list of predicted schwefel function for the remaning positions
    print(next_exp_dx, next_exp_dy, next_exp_pos)
    #return next_exp_pos[0], next_exp_pos[1], str(next_exp_pos)
    return next_exp_dx, next_exp_dy, str(next_exp_pos)

if __name__ == "__main__":
    d = DataUtilSim()
    url = "http://{}:{}".format(config['servers']['learningServer']
                                ['host'], config['servers']['learningServer']['port'])
    print('Port of ml Server: {}')
    uvicorn.run(app, host=config['servers']['learningServer']
                ['host'], port=config['servers']['learningServer']['port'])
    print("instantiated ml server")