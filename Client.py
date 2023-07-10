import requests

# Outgoing server API 
apiRequest = requests.get(API.API_URL, timeout=2000)  # Timeout after 2000 milliseconds
if apiRequest.status_code != 200:
    print(f'ERROR: Connection to API failed with code: {apiRequest.status_code}')
else:
    print(f'API connection is OK: {apiRequest.json}')
    