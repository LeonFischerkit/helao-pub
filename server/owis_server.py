import sys
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
from importlib import import_module
helao_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(helao_root, 'config'))
sys.path.append(os.path.join(helao_root, 'driver'))
from owis_driver import owis
config = import_module(sys.argv[1][:-3]).config


app = FastAPI(title="owis driver", 
            description= " this is a fancy owis driver server",
            version= "1.0")

class return_class(BaseModel):
    measurement_type: str = None
    parameters: dict = None
    data: dict = None

@app.get("/owis/activate")
def activate(motor:int=0):
    o.activate(motor)
    retc = return_class(parameters={"motor": motor},data= None)
    return retc
    
    

@app.get("/owis/configure")
def configure(motor:int=0):
    o.configure(motor)
    retc = return_class(parameters={"motor": motor},data=None)
    return retc

@app.get("/owis/move")
def move(count:int,motor:int=0,absol:bool=True):
    o.move(count,motor,absol)
    retc = return_class(parameters={"count": count, "motor": motor, "absol": absol,'units':{'count':'microsteps (about .0001mm)'}},data= None)
    return retc

@app.get("/owis/getPos")
def getPos():
    ret = o.getPos()
    retc = return_class(parameters=None,data= {"coordinates": ret,'units':{'coordinates':'microsteps (about .0001mm)'}})
    return retc

if __name__ == "__main__":
    o = owis(config['owis'])
    uvicorn.run(app, host=config['servers']['owisServer']['host'], port=config['servers']['owisServer']['port'])
    print("instantiated owis motor")
    