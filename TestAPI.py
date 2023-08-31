import requests
import HouseAPI

lightStateURL = HouseAPI.API_URL + "/light/state/"

        
def addParameter(url: str, id: int):
    return url + str(id)


r = requests.get(addParameter(lightStateURL, 1))
print(r.headers)
print(r.json())
# Use the following if micropython doesn't support .json()
#print(r.status_code)
#print(r.content)
if r.status_code == 200:
    if r.json() == 0:
        print(f'Light is OFF')
    else:
        print(f'Light is ON')
        
        
r2 = requests.put('http://127.0.0.1:8393/light/level/?id=8&newLightLevel=50.0')
