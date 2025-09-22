import requests
import json
from hashlib import sha1

url_user ="http://localhost:5050/"
url_file ="http://localhost:5051/"

input_user=input("Enter your name: ")
input_pswd=input("Enter your password: ")

username= {"username": input_user}
data= {"password": input_pswd}

response=requests.post(f"{url_user}create_user/{input_user}", json=data)

if response.status_code == 200:
    user_data=response.json()
    print("User created successfully:")
    print(json.dumps(user_data, indent=4))
else:
    print("Error creating user:", response.status_code, response.text)
    exit()
