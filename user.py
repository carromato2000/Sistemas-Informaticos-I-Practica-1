from quart import Quart, jsonify, request
import json
import os
import uuid

secret_uuid=uuid.UUID(hex='00010203-0405-0607-0809-0a0b0c0d0e0f')
app = Quart(__name__)



@app.route('/user/create/<name>', methods=['POST'])

async def create_user(name):
    try:
        file=open("users.txt", "r")
        for line in file:   # Si el usuario ya existe, no se puede crear
            user = json.loads(line)
            if user["name"] == name:
                file.close()
                return jsonify({"error": "User already exists"}), 400
        file.close()
    except FileNotFoundError:   # Si el archivo no existe, se crea uno nuevo
        pass
    file = open("users.txt", "a")
    
    data=await request.get_json()

    UID= uuid.uuid4()
    
    hash=uuid.uuid5(secret_uuid,str(UID))
    
    new_user ={
        "name": str(name),
        "psswd":str(data.get("password")),
        "id": str(UID),
        "hash": str(hash)
    }
    file.write(json.dumps(new_user)+"\n")
    file.close()
    return jsonify(new_user)

@app.route('/user/login/<name>', methods=['POST'])
async def get_user(user_id):
    return

if __name__ == '__main__':
    app.run(host='localhost', port=5050)


