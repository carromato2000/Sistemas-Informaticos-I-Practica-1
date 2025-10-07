
from quart import Quart, jsonify, request
import uuid
import os
import hashlib
from datetime import datetime, timedelta

secret_uuid=uuid.UUID(hex='00010203-0405-0607-0809-0a0b0c0d0e0f')
app = Quart(__name__)

def check_token(uid, token):
    return str(uuid.uuid5(secret_uuid,uid)) == token

@app.route('/file/<UID>/<filename>', methods=['GET'])
async def get_file(UID, filename):
    token = request.headers.get("token")

    try:
        file = open(f"{UID}/{filename}", "r")
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    public = file.readline() == "PUBLIC\n"
    if not public and not check_token(UID, token):
        file.close()
        return jsonify({"error": "File is private"}), 403
    
    content = file.read()
    file.close()
    return jsonify({"content": content})

@app.route('/file/<UID>/<filename>', methods=['PUT'])
async def put_file(UID, filename):
    data=await request.get_json()
    token = request.headers.get("token")
    if not check_token(UID, token):
        return jsonify({"error": "Invalid token"}), 403
    
    public = data.get("public", False)
    
    # Crear el directorio si no existe
    os.makedirs(f"{UID}", exist_ok=True)
    
    file = open(f"{UID}/{filename}", "w")
    if public:
        file.write("PUBLIC\n")
    else:
        file.write("PRIVATE\n")
    file.write(data.get("content", ""))
    file.close()
    return jsonify({"status": "File saved successfully"})

@app.route('/file/<UID>/<filename>', methods=['DELETE'])
async def delete_file(UID, filename):
    token = request.headers.get("token")
    if not check_token(UID, token):
        return jsonify({"error": "Invalid token"}), 403
    try:
        os.remove(f"{UID}/{filename}")
        return jsonify({"status": "File deleted successfully"})
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

@app.route('/file/<UID>', methods=['GET'])
async def list_files(UID):
    data=await request.get_json()
    token = request.headers.get("token")
    if not check_token(UID, token):
        return jsonify({"error": "Invalid token"}), 403
    try:
        files = os.listdir(f"{UID}/")
        return jsonify({"files": files})
    except FileNotFoundError:
        return jsonify({"error": "No files found for this user"}), 404
    
@app.route('/file/<UID>/<filename>/share', methods=['POST'])
async def share_file(UID,filename):
    token = request.headers.get("token")
    if not check_token(UID, token):
        return jsonify({"error": "Invalid token"}), 403
    now = datetime.now()
    one_minute_later = now + timedelta(minutes=1)
    
    time= one_minute_later.strftime("%Y-%m-%d %H:%M:%S")

    hash=hashlib.sha1(str(secret_uuid).encode()).hexdigest()
    
    share_token= str(UID)+"."+ filename +"."+ time +"."+ hash
    
    return jsonify({"share_token": share_token})

@app.route('/share/<share_token>', methods=['GET'])
async def access_shared_file(share_token):
    if not share_token:
        return jsonify({"error": "Share token is required"}), 400
    try:
        uid, filename, extension, expiry_time_str, token_hash = share_token.split('.')
        filename = filename + '.' + extension
    except ValueError:
        return jsonify({"error": "Invalid share token format"}), 400
    try:
        expiry_time = datetime.strptime(expiry_time_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return jsonify({"error": "Invalid expiry time format"}), 400    
    if datetime.now() > expiry_time:
        return jsonify({"error": "Share token has expired"}), 400
    hash_expected=hashlib.sha1(str(secret_uuid).encode()).hexdigest()
    if token_hash != hash_expected:
        return jsonify({"error": "Invalid share token hash"}), 400
    
    file=open(f"file/{uid}/{filename}", "r")
    content=file.read()
    file.close()
    return jsonify({"content": content})
    

    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5051)
    
    
    


