from fastapi import FastAPI, HTTPException

from HouseDatabase import HouseDatabase    # Store non-Personally Identifiable Information like house light status
import GlobalConstants as GC               # Global constants used across MainHouse.py, HouseDatabase.py, and PageKiteAPI.py

from time import sleep
import subprocess                   # Enable the running of CLI commands like "pip3 install -r requirements.txt"

API_PORT = '8393'
LOCAL_HOST = 'http://127.0.0.1'
API_URL = LOCAL_HOST + ':' + API_PORT

app = FastAPI()
db = HouseDatabase('Test.db')

@app.get('/')
async def root():
    return {'status': 'OK', 'data': f'API running at {API_URL}'}

@app.get('/light/state/{id}')
async def get_light_state(id: int) -> int:
    """ Get the state (HIGH or LOW) of a 1-based light ID in local SQLite database 
    
    Returns:
        JSON: {'status': ?, 'data':?}
    """
    result, foundData = db.query_table("LightStateTable")
    if id <= 0 or id > GC.MAX_LIGHT_BIT_LENGTH:
        foundData = False
    
    if foundData:
        row = id - 1
        return result[row][HouseDatabase.STATE_COLUMN_NUMBER]
    else:
        raise HTTPException(status_code=404, detail=f'ID = {id} primary key does NOT exists is the LightStateTable in database')
        #return {'status': 'INVALID', 'data': f'ID = {id} primary key does NOT exists is the LightStateTable in database'}


@app.get('/light/level/{id}')
async def get_light_level(id: int):
    """ Get the level (OFF, LOW, MEDIUM, or HIGH) of a 1-based light ID in local SQLite database 
    
    Returns:
        JSON data
    """
    result, foundData = db.query_table("LightLevelTable")
    if id <= 0 or id > GC.MAX_LIGHT_BIT_LENGTH:
        foundData = False
        
    if foundData:
        row = id - 1
        return result[row][HouseDatabase.LEVEL_COLUMN_NUMBER]
    else:
        raise HTTPException(status_code=404, detail=f'ID = {id} primary key does NOT exists is the LightLevelTable in database')

@app.put('/log/')
async def log(message: str):
    db.insert_debug_logging_table(message)


# Use http://127.0.0.1:8393/docs to send PUT commands
# Or curl -X PUT http://127.0.0.1:8393/light/level/\?id\=8\&newLightLevel\=0
@app.put('/light/level/')
async def update_light_level(id: int, newLightLevel: float):
    validId = True
    if id <= 0 or id > GC.MAX_LIGHT_BIT_LENGTH:
        validId = False
    
    if validId:
        db.update_light_level_table(id, newLightLevel)
        return {'updated': id}
    else:
        raise HTTPException(status_code=404, detail=f'ID = {id} primary key does NOT exists is the LightLevelTable in database')


def start_api() -> int:
    """Use UVicorn a fast ASGI (Asynchronous Server Gateway Interface) to running auto refreshing API
       Get a list of ASGI processes running "lsof -i :8000" and kill using "kill -9 ?????"
    """
    
    command = ['uvicorn', 'HouseAPI:app', '--host', '0.0.0.0', '--reload', '--port', API_PORT]
    backgroundApiProcess = subprocess.Popen(command)
    processCode = backgroundApiProcess.pid
    db.insert_debug_logging_table(f'PID = {processCode} API URL = {API_URL}')
    sleep(3)       # Delay to give API server to start up  
    
    return int(processCode)


if __name__ == "__main__":
    apiBackgroundProcessCode = start_api()
    
    try:
        while True:
            pass
        
    except KeyboardInterrupt:
        command = ['kill', '-9', str(apiBackgroundProcessCode)]
        subprocess.call(command)
        
        # Sleep so that only single 'Ctrl+C' is needed to exit program
        sleep(3)                    
        raise SystemExit
