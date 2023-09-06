import requests
import HouseAPI

def addGetParameter(url: str, id: int):
    return HouseAPI.API_URL + url + str(id)

def addPutParameter(url: str, allParameters: list):
    urlFragmentIdentifier = ''
    for i in range(int(len(allParameters)/2)):
        if i >= 1:
            urlFragmentIdentifier = urlFragmentIdentifier + '&'
        urlFragmentIdentifier = urlFragmentIdentifier + str(allParameters[2*i]) + '=' + str(allParameters[2*i+1]) 
    
    return HouseAPI.API_URL + url + '?' + urlFragmentIdentifier

def logParameter():
    pass


r1 = requests.get(addGetParameter( "/light/level/", 1))
print(r1.headers)
print(r1.json())
# Use the following if micropython doesn't support .json()
#print(r1.status_code)
#print(r1.content)
if r1.status_code == 200:
    if r1.json() == 0:
        print(f'Light is OFF')
    else:
        print(f'Light is ON')
elif r1.status_code == 422:
    print('Typo in URL or parameters')

newLightLevel = 69.0
r2 = requests.put(addPutParameter( "/light/level/", ['isd', 7, 'newLightLevel', newLightLevel]))
if r2.status_code == 200:
    print(f'Changing light level to {newLightLevel}')
elif r2.status_code == 422:
    r = requests.put(HouseAPI.API_URL + '/log/?message="Typo in URL or parameters"')
    
r3 = requests.put('http://127.0.0.1:8393/light/level/?id=8&newLightLevel=50.0')
