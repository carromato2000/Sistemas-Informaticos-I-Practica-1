from quart import Quart, jsonify, request
import uuid
import model
import os

from exceptions import UserAlreadyExistsError, UserNotFoundError, InvalidCredentialsError

secret_uuid=uuid.UUID(hex='00010203-0405-0607-0809-0a0b0c0d0e0f')
app = Quart(__name__)

def validate_token():
    """
    Valida el token de autorización de la cabecera de la petición.
    Retorna el user_id si el token es válido, None en caso contrario.
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return False
    
    if not auth_header.startswith('Bearer '):
        return False
    auth_header = auth_header[7:]  # Elimina "Bearer "

    auth_header = auth_header.split('.')
    if len(auth_header) != 2:
        return False
    [userid , token] = auth_header
    
    # Genera el token esperado para este usuario
    expected_token = str(uuid.uuid5(secret_uuid, str(userid)))
    
    if token == expected_token:
        return userid
    else:
        return None

@app.route('/users', methods=['POST'])
async def create_user():
    data=await request.get_json()
    name=data.get("name")
    password=data.get("password")
    if not name:
        return jsonify({"error": "Name data is empty"}), 400
    if not password:
        return jsonify({"error": "Password data is empty"}), 400
    if len(password)<4:
        return jsonify({"error": "Password must be at least 4 characters"}), 400

    try:
        user = await model.create_user(name, password)
    except UserAlreadyExistsError:
        return jsonify({"error": "User already exists"}), 409

    uid = str(user.userid)
    token = uid +'.'+str(uuid.uuid5(secret_uuid, str(user.userid)))

    body = {
        "uid": uid,
        "token": token
    }

    return jsonify(body), 200

@app.route('/login', methods=['POST'])
async def get_user():
    data = await request.get_json()
    name = data.get("name")
    password = data.get("password")

    try:
        user = await model.get_user(name, password)
    except UserNotFoundError:
        return jsonify({"error": "User not found"}), 404
    except InvalidCredentialsError:
        return jsonify({"error": "Invalid credentials"}), 401
    
    uid = str(user.apiid)
    token = uid+'.'+str(uuid.uuid5(secret_uuid, uid))

    body = {
        "uid": uid,
        "token": token
    }

    return jsonify(body), 200

@app.route('/users/<userid>', methods=['PATCH'])
async def update_password(userid):
    """
    Permitira cambiar la contrasena del usuario autenticado.
    """
    auth_userid = validate_token()
    if auth_userid is None or auth_userid != userid:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = await request.get_json()
    password=data.get("password")
    if not password:
        return jsonify({"error": "New password data is empty"}), 400
    if len(password)<4:
        return jsonify({"error": "Password must be at least 4 characters"}), 400
    
    try:
        await model.update_password(userid, password)
    except UserNotFoundError:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({"message": "Password updated successfully"}), 200
    

@app.route('/users/<userid>', methods=['DELETE'])
async def delete_user(userid):
    auth_userid = validate_token()
    if auth_userid is None:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        await model.delete_user(userid, auth_userid)
    except PermissionError:
        return jsonify({"error": "Unauthorized: Admin privileges required"}), 403
    except UserNotFoundError: 
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"}), 200

@app.route('/users/<userid>/balance', methods=['POST'])
async def add_credit(userid):
    # Validación del token
    auth_userid = validate_token()
    if auth_userid is None or auth_userid != userid:
        return jsonify({"error": "Unauthorized"}), 401

    data= await request.get_json()
    amount = data.get("amount")
    if not amount:
        return jsonify({"error": "Amount data is empty"}), 400
    try:
        amount = float(amount)
    except ValueError:
        return jsonify({"error": "Amount must be a number"}), 400
    if amount <= 0:
        return jsonify({"error": "Amount must be positive"}), 400
    if round(amount, 2) != amount:
        return jsonify({"error": "Amount must have at most two decimal places"}), 400

    try:
        user= await model.update_credit(userid, amount)
    except UserNotFoundError:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"new_credit": f"{user.balance}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)


