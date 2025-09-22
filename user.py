from quart import Quart, jsonify, request

import uuid


app = Quart(__name__)



@app.route('/create_user/<name>', methods=['POST'])

async def create_user(name):
    
    file=open("users.txt", "a")
    if not file:
        return jsonify({"error": "Could not open file"}), 500
    
    data=await request.get_json()
    
    UID= uuid.uuid4()
    secret_uuid=uuid.UUID(str(name))
    hash=uuid.uuid5(secret_uuid,str(UID))
    
    new_user ={
        "name": str(name),
        "psswd":str(data.get("password")),
        "id": str(UID),
        "hash": str(hash)
    }
    file.write(f"{str(new_user)}\n")
    file.close()
    return jsonify(new_user)

if __name__ == '__main__':
    app.run(host='localhost', port=5050)


