import requests
import json
from hashlib import sha1

url_user ="http://localhost:5050/"
url_file ="http://localhost:5051/"

print("Client Application")
print("1. Create User")
print("2. Login User")
choice=input("Select an option (1 or 2): ")

if choice not in ['1','2']:
    print("Invalid option. Exiting.")
    exit()

elif choice =='1':

    input_user=input("Enter your name: ")
    input_pswd=input("Enter your password: ")

    data= {"name": input_user,"psswd": input_pswd}

    response=requests.post(f"{url_user}/user/create", json=data)

    if response.status_code == 200:
        user_data=response.json()
        print("User created successfully:")
        print(json.dumps(user_data, indent=4))
    else:
        print("Error creating user:", response.status_code, response.text)
        exit()

elif choice =='2':

    input_user=input("Enter your name: ")
    input_pswd=input("Enter your password: ")

    data= {"name": input_user,"psswd": input_pswd}

    response=requests.post(f"{url_user}/user/login", json=data)

    if response.status_code == 200:
        user_data=response.json()
        print("User logged in successfully:")
        print(json.dumps(user_data, indent=4))
        
        ##Acceso a ficheros
        print("\nFile Operations")
        print("1. Read File")
        print("2. List Files")
        print("3. Edit/Create File")
        print("4. Delete File")
        file_choice=input("Select an option (1, 2, 3 or 4): ")
        if file_choice not in ['1','2','3','4']:
            print("Invalid option. Exiting.")
            exit()
        
        if file_choice =='1':
            filename=input("Enter the filename to read: ")
            
            response=requests.get(f"{url_file}/file/{user_data.get('id')}/{filename}", json=user_data)
            if response.status_code == 200:
                file_content=response.json()
                print("File content:")
                print(json.dumps(file_content, indent=4))
            else:
                print("Error reading file:", response.status_code, response.text)
                exit()
        elif file_choice =='2':
            response=requests.get(f"{url_file}/file/{user_data.get('id')}", json=user_data)
            if response.status_code == 200:
                files_list=response.json()
                print("Files list:")
                print(json.dumps(files_list, indent=4))
            else:
                print("Error listing files:", response.status_code, response.text)
                exit()
        elif file_choice =='3':
            filename=input("Enter the filename to edit/create: ")
            content=input("Enter the content to write in the file: ")
            user_data['content']=content
            
            response=requests.put(f"{url_file}/file/{user_data.get('id')}/{filename}", json=user_data)
            if response.status_code == 200:
                result=response.json()
                print("File edited/created successfully:")
                print(json.dumps(result, indent=4))
            else:
                print("Error editing/creating file:", response.status_code, response.text)
                exit()
        elif file_choice =='4':
            filename=input("Enter the filename to delete: ")
            
            response=requests.delete(f"{url_file}/file/{user_data.get('id')}/{filename}", json=user_data)
            if response.status_code == 200:
                result=response.json()
                print("File deleted successfully:")
                print(json.dumps(result, indent=4))
            else:
                print("Error deleting file:", response.status_code, response.text)
                exit()
    else:
        print("Error logging in:", response.status_code, response.text)
        exit()
