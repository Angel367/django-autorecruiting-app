import requests


req1 = requests.get(url='http://127.0.0.1:5000/resumes')
if req1.status_code == 200:
    print("OK")

req = requests.get(url='http://127.0.0.1:5000/resumes/1')
if req.status_code == 200:
    print("OK")

assert req1.json()['items'][0]['first_name'] == req.json()['first_name']