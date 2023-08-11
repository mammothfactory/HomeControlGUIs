from fastapi import FastAPI

from HouseDatabase import HouseDatabase    # Store non-Personally Identifiable Information like house light status
import GlobalConstants as GC               # Global constants used across MainHouse.py, HouseDatabase.py, and PageKiteAPI.py

API_PORT = '8000' #'8393'
LOCAL_HOST = 'http://127.0.0.1'
API_URL = LOCAL_HOST + ':' + API_PORT

app = FastAPI()
db = HouseDatabase()

@app.get('/')
async def root():
    return {'status': 'OK', 'code': 200}

@app.get('/lights/')
async def lights():
    """ Get newest database entry (at row 0) for current state of lights

    Returns:
        JSON: HTTP Status Code and binary levels for 8 lights in a litehouse
    """
    row = db.query_table("LightStateTable")
    if len(row) > 0:
        return {'status': 'OK', 'data': row[0][HouseDatabase.BINARY_STATE_COLUMN_NUMBER]}
    else:
        return {'status': 'OK', 'data': 0b0000_0000}

# https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/418
