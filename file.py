from quart import Quart, jsonify, request
import uuid
import os

secret_uuid=uuid.UUID(hex='00010203-0405-0607-0809-0a0b0c0d0e0f')
app = Quart(__name__)

def check_token(uid, token):
    return str(uuid.uuid5(secret_uuid,uid)) == token

@app.route('/file/<UID>/<filename>', methods=['GET'])
async def get_file(UID, filename):
    data=await request.get_json()
    if not check_token(data.get("id"), data.get("token")):
        return jsonify({"error": "Invalid token"}), 403
        
    try:
        file = open(f"file/{UID}/{filename}", "r")
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    
    content = file.read()
    file.close()
    return jsonify({"content": content})

@app.route('/file/<UID>/<filename>', methods=['PUT'])
async def put_file(UID, filename):
    data=await request.get_json()
    if not check_token(data.get("id"), data.get("token")):
        return jsonify({"error": "Invalid token " + data.get("token")}), 403
    
    # Crear el directorio si no existe
    os.makedirs(f"file/{UID}", exist_ok=True)
    
    file = open(f"file/{UID}/{filename}", "w")
    file.write(data.get("content", ""))
    file.close()
    return jsonify({"status": "File saved successfully"})

@app.route('/file/<UID>/<filename>', methods=['DELETE'])
async def delete_file(UID, filename):
    data=await request.get_json()
    if not check_token(data.get("id"), data.get("token")):
        return jsonify({"error": "Invalid token"}), 403
    try:
        os.remove(f"file/{UID}/{filename}")
        return jsonify({"status": "File deleted successfully"})
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

@app.route('/file/<UID>', methods=['GET'])
async def list_files(UID):
    data=await request.get_json()
    if not check_token(data.get("id"), data.get("token")):
        return jsonify({"error": "Invalid token"}), 403
    try:
        files = os.listdir(f"file/{UID}/")
        return jsonify({"files": files})
    except FileNotFoundError:
        return jsonify({"error": "No files found for this user"}), 404
    
@app.route('/file/<UID>/<filename>/share', methods=['POST'])
async def share_file(UID,filename):
    data = await request.get_json()
    if not check_token(data.get("id"), data.get("token")):
        return jsonify({"error": "Invalid token"}), 403
    

    
    
if __name__ == '__main__':
    app.run(host='localhost', port=5051)
    
    
    


