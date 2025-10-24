from quart import Quart, jsonify, request
import uuid
import model

secret_uuid=uuid.UUID(hex='00010203-0405-0607-0809-0a0b0c0d0e0f')
app = Quart(__name__)

def validate_token():
    """
    Valida el token de autorización de la cabecera de la petición.
    Retorna True si el token es válido, False en caso contrario.
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return False
    
    if auth_header.startswith('Bearer '):
        auth_header = auth_header[7:]  # Elimina "Bearer "

    try:
        user_id , token = auth_header.split('.')
    except ValueError:
        return False
    
    # Genera el token esperado para este usuario
    expected_token = str(uuid.uuid5(secret_uuid, str(user_id)))
    
    return token == expected_token

@app.route('/movies', methods=['GET'])
async def get_movies():
    """
    Retorna una película o conjunto de películas del catálogo
    """
    title = request.args.get('title')
    year = request.args.get('year')
    genre = request.args.get('genre')
    actor = request.args.get('actor')
    if year is not None:
        try:
            year = int(year)
        except ValueError:
            return jsonify({"error": "Year must be an integer"}), 400
    movies = await model.get_movies(title=title, year=year, genre=genre, actor=actor)
    return jsonify(movies), 200

@app.route('/movies/<movieid>', methods=['GET'])
async def get_movie(movieid):
    """
    Retorna los detalles de una película específica del catálogo
    """
    return jsonify({"message": "Funcionalidad no implementada aún"}), 501

@app.route('/cart', methods=['GET'])
async def get_cart():
    """
    Retorna el contenido del carrito de compras
    """
    return jsonify({"message": "Funcionalidad no implementada aún"}), 501

@app.route('/cart/<movieid>', methods=['PUT'])
async def add_movie_to_cart(movieid):
    """
    Añade una película al carrito
    """
    return jsonify({"message": "Funcionalidad no implementada aún"}), 501

@app.route('/cart/<movieid>', methods=['DELETE'])
async def remove_movie_from_cart(movieid):
    """
    Elimina una película del carrito
    """
    return jsonify({"message": "Funcionalidad no implementada aún"}), 501

@app.route('/cart/checkout', methods=['POST'])
async def checkout_cart():
    """
    Paga el contenido del carrito de compras con el saldo.
    """
    return jsonify({"message": "Funcionalidad no implementada aún"}), 501

@app.route('/orders/<orderid>', methods=['GET'])
async def get_order(orderid):
    return jsonify({"message": "Funcionalidad no implementada aún"}), 501


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5051)