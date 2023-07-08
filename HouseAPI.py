API_PORT = '8000' #'8393'
LOCAL_HOST = 'http://127.0.0.1'
API_URL = LOCAL_HOST + ':' + API_PORT

from fastapi import FastAPI


app = FastAPI()

@app.get('/') 
async def root():
    return {'status': 'OK', 'code': 200}



# https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/418
