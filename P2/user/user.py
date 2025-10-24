from quart import Quart, jsonify, request
import uuid
import model

from exceptions import UserAlreadyExistsError, UserNotFoundError, InvalidCredentialsError

secret_uuid=uuid.UUID(hex='00010203-0405-0607-0809-0a0b0c0d0e0f')
app = Quart(__name__)

def validate_token(user_id):
    """
    Valida el token de autorización de la cabecera de la petición.
    Retorna True si el token es válido, False en caso contrario.
    """
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return False
    
    # El formato típico es "Bearer <token>" o simplemente "<token>"
    token = auth_header
    if auth_header.startswith('Bearer '):
        token = auth_header[7:]  # Elimina "Bearer "
    
    # Genera el token esperado para este usuario
    expected_token = str(uuid.uuid5(secret_uuid, str(user_id)))
    
    return token == expected_token


def validate_token(user_id):
    """
    Valida el token de autorización de la cabecera de la petición.
    Retorna True si el token es válido, False en caso contrario.
    """
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return False
    
    # El formato típico es "Bearer <token>" o simplemente "<token>"
    token = auth_header
    if auth_header.startswith('Bearer '):
        token = auth_header[7:]  # Elimina "Bearer "
    
    # Genera el token esperado para este usuario
    expected_token = str(uuid.uuid5(secret_uuid, str(user_id)))
    
    return token == expected_token

@app.route('/user', methods=['PUT'])

async def create_user():
    data=await request.get_json()
    name=data.get("name")
    password=data.get("password")
    if not name:
        return jsonify({"error": "Name data is empty"}), 404 

    elif not password:
        return jsonify({"error": "Password data is empty"}), 404

    try:
        user = await model.create_user(name, password)
    except UserAlreadyExistsError:
        return jsonify({"error": "User already exists"}), 409

    uid = str(user.id)
    token = uid +'.'+str(uuid.uuid5(secret_uuid, str(user.id)))

    body = {
        "uid": uid,
        "token": token
    }

    return jsonify(body), 200

@app.route('/user', methods=['GET'])
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
    
    uid = str(user.id)
    token = uid+'.'+str(uuid.uuid5(secret_uuid, str(user.id)))

    body = {
        "uid": uid,
        "token": token
    }

    return jsonify(body), 200

@app.route('/user/<userid>', methods=['PATCH'])
async def update_password(userid):
    """
    Permitira cambiar la contrasena del usuario autenticado.
    """
    return jsonify({"message": "Funcionalidad no implementada aún"}), 501

@app.route('/user/<userid>', methods=['DELETE'])
async def delete_user(userid):
    return jsonify({"message": "Funcionalidad no implementada aún"}), 501

@app.route('/user/credit', methods=['POST'])
async def add_credit():
    return jsonify({"message": "Funcionalidad no implementada aún"}), 501

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)


