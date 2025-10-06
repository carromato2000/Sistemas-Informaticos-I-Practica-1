from quart import Quart, jsonify, request
import json
import os
import uuid

secret_uuid=uuid.UUID(hex='00010203-0405-0607-0809-0a0b0c0d0e0f')
app = Quart(__name__)



@app.route('/user/create', methods=['POST'])

async def create_user():
    data=await request.get_json()
    name=data.get("name")
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
    
    UID=uuid.uuid4()
    token=uuid.uuid5(secret_uuid,str(UID))
    
    new_user ={
        "name": name,
        "psswd":str(data.get("psswd")),
        "id": str(UID),
        "token": str(token)
    }
    file.write(json.dumps(new_user)+"\n")
    file.close()
    del new_user["psswd"]  # No se devuelve la contraseña
    del new_user["name"]  # No se devuelve el nombre
    return jsonify(new_user)

@app.route('/user/login', methods=['POST'])
async def get_user():
    data = await request.get_json()
    name = data.get("name")
    try:
        file=open("users.txt", "r")
        for line in file:
            user = json.loads(line)
            if user["name"] == name:
                file.close()
                if user["psswd"] != data.get("psswd"):
                    return jsonify({"error": "incorrect password"}), 404
                else:
                    del user["psswd"]  # No se devuelve la contraseña
                    del user["name"]  # No se devuelve el nombre
                    return jsonify(user)
        file.close()
        return jsonify({"error": "User not found"}), 404
    except FileNotFoundError:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)


