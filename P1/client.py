import requests
import json
from hashlib import sha1
import uuid

url_user ="http://localhost:5050/"
url_file ="http://localhost:5051/"

name = "alice"
psswd = "password123"

data= {"name": name,"psswd": psswd}

def manage_response(response):
    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Error:", response.status_code, response.json())

#Create user repeated
response=requests.post(f"{url_user}/user/create", json=data)
manage_response(response)

#Name empty
response=requests.post(f"{url_user}/user/create", json={"name": "", "psswd": psswd})
manage_response(response)

#Password empty
response=requests.post(f"{url_user}/user/create", json={"name": "david", "psswd": ""})
manage_response(response)

#Incorrect psswd
response=requests.post(f"{url_user}/user/login", json={"name": "david", "psswd": "1235"})
manage_response(response)

#Login success
response=requests.post(f"{url_user}/user/login", json={"name": name, "psswd": psswd})
manage_response(response)

#User and file example data
user_data=response.json()
id = user_data["id"]
token = user_data["token"]
filename = "example.txt"
content = "This is an example file content."
headers = {"token": token}

data = {"content": content, "public": False}

#Create file
response=requests.put(f"{url_file}file/{id}/{filename}", json=data, headers=headers)
manage_response(response)

data.pop("public")

#Failed access to private file
response=requests.get(f"{url_file}file/{id}/{filename}", headers={"token": "invalid_token"}, json=data)
manage_response(response)

#Success access to private file
response=requests.get(f"{url_file}file/{id}/{filename}", headers=headers, json=data)
manage_response(response)

#Success access to list of files
response=requests.get(f"{url_file}file/{id}", json=data, headers= headers)
manage_response(response)

#Delete file success
response=requests.delete(f"{url_file}file/{id}/{filename}", headers=headers,json=data)
manage_response(response)

response=requests.get(f"{url_file}file/{id}", json=data, headers= headers)
manage_response(response)

response=requests.put(f"{url_file}file/{id}/{filename}", json=data, headers=headers)
manage_response(response)
response=requests.get(f"{url_file}file/{id}", json=data, headers= headers)
manage_response(response)
#Share
response=requests.post(f"{url_file}file/{id}/{filename}/share", json=data, headers= headers)
manage_response(response)

user_data= response.json()
share_token= user_data.get("share_token")

response=requests.get(f"{url_file}/share/{share_token}")
manage_response(response)

