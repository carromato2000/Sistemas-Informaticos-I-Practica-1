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
        print("Error:", response.status_code, response.text)
        exit()

response=requests.post(f"{url_user}/user/create", json=data)
manage_response(response)

response=requests.post(f"{url_user}/user/login", json={"name": name, "psswd": psswd})
manage_response(response)

user_data=response.json()
id = user_data["id"]
token = user_data["token"]
filename = "example.txt"
content = "This is an example file content."

data = {"id": id, "token": token, "content": content}

response=requests.put(f"{url_file}file/{id}/{filename}", json=data)
manage_response(response)

response=requests.get(f"{url_file}file/{id}", json={"id": id, "token": token})
manage_response(response)

response=requests.delete(f"{url_file}file/{id}/{filename}", json={"id": id, "token": token})
manage_response(response)