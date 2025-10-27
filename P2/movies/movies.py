from quart import Quart, jsonify, request
import uuid

import model
from exceptions import *
from datetime import date

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
    if title is not None:
        try:
            title=str(title).title()
        except ValueError:
            return jsonify({"error": "Title must be a string"}), 400
    if actor is not None:
        try:
            actor=str(actor).title()
        except ValueError:
            return jsonify({"error": "Actor must be a string"}), 400
    if year is not None:
        try:
            year = int(year)
        except ValueError:
            return jsonify({"error": "Year must be an integer"}), 400
    movies = await model.get_movies(title=title, year=year, genre=genre, actor=actor)
    return jsonify(movies), 200

@app.route('/movies', methods=['PUT'])
async def add_movie():
    """
    Añade una nueva película al catálogo
    """
    # Verificar token y obtener el uid del usuario que hace la peticion
    if not validate_token():
        return jsonify({"error": "Unauthorized"}), 401
    uid = request.headers.get('Authorization').split(' ')[1].split('.')[0]
    if not await model.validate_admin(uid):
        return jsonify({"error": "User is not admin"}), 401


    # Obtener los parametros de la peticion, donde esta el titulo, genero y precio de la pelicula
    title= request.args.get("title")
    # La pelicula debe tener un titulo
    if not title:
        return jsonify({"error": "Title data is empty"}), 400
    year_data= request.args.get("year")
    # La pelicula debe tener un año
    if not year_data:
        return jsonify({"error": "Year data is empty"}), 400
    price_data= request.args.get("price")
    # La pelicula debe tener un precio
    if not price_data:
        return jsonify({"error": "Price data is empty"}), 400
    genre= request.args.get("genre")
    if not genre:
        return jsonify({"error": "Genre data is empty"}), 400

    try:
        year = int(year_data)
    except ValueError:
        return jsonify({"error": "Year must be an integer"}), 400
    try:
        price = float(price_data)
        if price < 0:
            return jsonify({"error": "Price must be non-negative"}), 400
    except ValueError:
        return jsonify({"error": "Price must be a number"}), 400

    # Obtenemod la descripcion del cuerpo de la peticion
    data= await request.get_json()
    # Si no hay cuerpo o no tiene descripcion, ponemos la cadena vacia
    if data is None:
        description=""
    else:
        description= data.get("description")
        if description is None:
            description=""
    
    try:
        movieid= await model.add_movie(title, year, genre, description, price)
    except MovieAlreadyExistsError:
        return jsonify({"error": "Movie already exists"}), 409
    if movieid is None:
        return jsonify({"error": "Failed to add movie"}), 500
    return jsonify({"movieid": movieid}), 201

@app.route('/actors', methods=['PUT'])
async def add_actor():
    """
    Añade un nuevo actor a la base de datos
    """
    if not validate_token():
        return jsonify({"error": "Unauthorized"}), 401
    uid = request.headers.get('Authorization').split(' ')[1].split('.')[0]
    if not await model.validate_admin(uid):
        return jsonify({"error": "User is not admin"}), 401
    
    name= request.args.get("name")
    if not name:
        return jsonify({"error": "Name data is empty"}), 400
    birthdate= request.args.get("birthdate")
    if not birthdate:
        return jsonify({"error": "Birthdate data is empty"}), 400
    
    try:
        birthdate = date.fromisoformat(birthdate)
    except ValueError:
        return jsonify({"error": "Birthdate must be in YYYY-MM-DD format"}), 400
    try:
        actorid= await model.add_actor(name, birthdate)
    except ActorAlreadyExistsError:
        return jsonify({"error": "Actor already exists"}), 409
    if actorid is None:
        return jsonify({"error": "Failed to add actor"}), 500
    return jsonify({"actorid": actorid}), 201

@app.route('/actors', methods=['GET'])
async def get_actors():
    """
    Retorna un actor o conjunto de actores de la base de datos
    """
    name = request.args.get('name')
    actors = await model.get_actors(name=name)
    return jsonify(actors), 200

@app.route('/actors/<actorid>', methods=['DELETE'])
async def get_actor(actorid):
    """
    Elimina un actor de la base de datos
    """
    # Verificar token y obtener el uid del usuario que hace la peticion
    if not validate_token():
        return jsonify({"error": "Unauthorized"}), 401
    uid = request.headers.get('Authorization').split(' ')[1].split('.')[0]
    if not await model.validate_admin(uid):
        return jsonify({"error": "User is not admin"}), 401

    try:
        int(actorid)
    except ValueError:
        return jsonify({"error": "Invalid actor ID format"}), 400

    try:
        await model.delete_actor(int(actorid))
    except ActorNotFoundError:
        return jsonify({"error": "Actor not found"}), 404
    return jsonify({"message": "Actor deleted successfully"}), 200

@app.route('/movies/<movieid>', methods=['DELETE'])
async def delete_movie(movieid):
    """
    Elimina una película del catálogo
    """
    # Verificar token y obtener el uid del usuario que hace la peticion
    if not validate_token():
        return jsonify({"error": "Unauthorized"}), 401
    uid = request.headers.get('Authorization').split(' ')[1].split('.')[0]
    if not await model.validate_admin(uid):
        return jsonify({"error": "User is not admin"}), 401

    try:
        int(movieid)
    except ValueError:
        return jsonify({"error": "Invalid movie ID format"}), 400

    try:
        await model.delete_movie(int(movieid))
    except MovieNotFoundError:
        return jsonify({"error": "Movie not found"}), 404
    return jsonify({"message": "Movie deleted successfully"}), 200

@app.route('/movies/<movieid>', methods=['GET'])
async def get_movie(movieid):
    """
    Retorna los detalles de una película específica del catálogo
    """
    if not movieid.isdigit():
        return jsonify({"error": "Invalid movie ID format"}), 400
    movie= await model.get_movie_by_id(int(movieid))
    if not movie:
        return jsonify({"error": "Movie not found"}), 404
    print("[DEBUG] Movie found:", movie)
    return jsonify(movie), 200
        

@app.route('/cart', methods=['GET'])
async def get_cart():
    """
    Retorna el contenido del carrito de compras
    """
    if not validate_token():
        return jsonify({"error": "Unauthorized"}), 401
    headers = request.headers.get('Authorization')
    user_id = headers.split(' ')[1].split('.')[0]
    movie= await model.get_carts(user_id)
   
    return jsonify(movie), 200

@app.route('/cart/<movieid>', methods=['PUT'])
async def add_movie_to_cart(movieid):
    """
    Añade una película al carrito
    """
    if not validate_token():
        return jsonify({"error": "Unauthorized"}), 401
    if movieid is None:
        return jsonify({"error": "Movie ID is required"}), 400
    if not movieid.isdigit():
        return jsonify({"error": "Invalid movie ID format"}), 400
    headers = request.headers.get('Authorization')
    user_id = headers.split(' ')[1].split('.')[0]
    movie_not_in_cart=await model.add_movie_to_cart(user_id, int(movieid))
    if not movie_not_in_cart:
        return jsonify({"error": "Movie already in cart"}), 409
    else:
        return jsonify({"message": "Movie added to cart"}), 200

@app.route('/cart/<movieid>', methods=['DELETE'])
async def delete_movie_from_cart(movieid):
    """
    Elimina una película del carrito
    """
    if not validate_token():
        return jsonify({"error": "Unauthorized"}), 401
    if movieid is None:
        return jsonify({"error": "Movie ID is required"}), 400
    if not movieid.isdigit():
        return jsonify({"error": "Invalid movie ID format"}), 400
    headers = request.headers.get('Authorization')
    user_id = headers.split(' ')[1].split('.')[0]
    movie_in_cart=await model.delete_movie_from_cart(user_id, int(movieid))
    if not movie_in_cart:
        return jsonify({"error": "Movie not in cart"}), 404
    else:
        return jsonify({"message": "Movie removed from cart"}), 200
    

@app.route('/cart/checkout', methods=['POST'])
async def checkout_cart():
    """
    Paga el contenido del carrito de compras con el saldo.
    """
    if not validate_token():
        return jsonify({"error": "Unauthorized"}), 401
    headers = request.headers.get('Authorization')
    user_id = headers.split(' ')[1].split('.')[0]
    order= await model.checkout_cart(user_id)
    if order == -1:
        return jsonify({"error": "User not found"}), 404
    elif order == -2:
        return jsonify({"error": "Cart is empty"}), 404
    elif order == -3:
        return jsonify({"error": "Insufficient funds"}), 402
    elif order.get("orderid") is None:
        return jsonify({"error": "Order creation failed"}), 500
    else:
        return jsonify(order), 200

@app.route('/orders/<orderid>', methods=['GET'])
async def get_order(orderid):
    if not validate_token():
        return jsonify({"error": "Unauthorized"}), 401
    if orderid is None:
        return jsonify({"error": "Order ID is required"}), 400
    if not orderid.isdigit():
        return jsonify({"error": "Invalid order ID format"}), 400
    order= await model.get_order_by_id(int(orderid))
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order), 200
    

@app.route('/user/credit', methods=['POST'])
async def add_credit():
    if not validate_token():
        return jsonify({"error": "Unauthorized"}), 401
    headers = request.headers.get('Authorization')
    user_id = headers.split(' ')[1].split('.')[0]
    data= await request.get_json()
    amount_data= data.get("amount")
    
    if not amount_data:
        return jsonify({"error": "Amount data is empty"}), 404 
    try:
        amount = float(amount_data)
    except ValueError:
        return jsonify({"error": "Amount must be a number"}), 400
    if amount <= 0:
        return jsonify({"error": "Amount must be positive"}), 400
    
    new_balance= await model.update_credit(user_id, amount)
    if new_balance == -1:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"new_credit": f"{new_balance}"}), 200

@app.route('/user/credit/<amount>', methods=['POST'])
async def set_credit(amount):
    if not validate_token():
        return jsonify({"error": "Unauthorized"}), 401
    headers = request.headers.get('Authorization')
    user_id = headers.split(' ')[1].split('.')[0]
    try:
        amount_value = float(amount)
    except ValueError:
        return jsonify({"error": "Amount must be a number"}), 400
    if amount_value < 0:
        return jsonify({"error": "Amount must be non-negative"}), 400
    
    current_balance= await model.set_credit(user_id, amount_value)
    if current_balance == -1:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({"new_credit": f"{current_balance}"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5051)