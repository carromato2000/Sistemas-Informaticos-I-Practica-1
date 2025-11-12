from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from exceptions import *


usuario= 'alumnodb'
contraseña= '1234'
host='db'
port= '5432'
database='si1'

url_conexion=f'postgresql+asyncpg://{usuario}:{contraseña}@{host}:{port}/{database}'
engine=create_async_engine(url_conexion, echo=True)

async def get_user_by_uid(uid: str):
    async with engine.connect() as conn:
        result = await conn.execute(text(
            "SELECT * FROM get_user_by_apiid(:apiid)"
        ), {"apiid": uid})
        user = result.fetchone()
        if not user:
            raise NotFoundError("User not found")
        return dict(user._mapping)

async def get_user_id(uid: str):
    try:
        user = await get_user_by_uid(uid)
        return user.get("userid")
    except NotFoundError:
        raise NotFoundError("User not found")
    
async def validate_admin(uid: str):        
    try:
        user = await get_user_by_uid(uid)
        return user.get("name") == "admin"
    except NotFoundError:
        return False


async def get_movies(title = None, year = None, genre = None, actor = None):
    async with engine.connect() as conn:
        if actor is None:
            result = await conn.execute(text(
                "SELECT * FROM movie "
                "WHERE (CAST(:title AS VARCHAR) IS NULL OR title = :title) "
                "AND (CAST(:year AS INT) IS NULL OR year = :year) "
                "AND (CAST(:genre AS VARCHAR) IS NULL OR genre = :genre)"
            ), {"title": title, "year": year, "genre": genre})
        
        else:
            result = await conn.execute(text(
                "SELECT DISTINCT m.* FROM movie m "
                "JOIN casts c ON m.movieid = c.movie "
                "JOIN actor a ON c.actor = a.actorid "
                "WHERE a.name = :actor "
                "AND (CAST(:title AS VARCHAR) IS NULL OR m.title = :title) "
                "AND (CAST(:year AS INT) IS NULL OR m.year = :year) "
                "AND (CAST(:genre AS VARCHAR) IS NULL OR m.genre = :genre)"
            ), {"title": title, "year": year, "genre": genre, "actor": actor})
        return [dict(row._mapping) for row in result.fetchall()]
    
async def get_top_movies(top: int = 10):
    async with engine.connect() as conn:
        result = await conn.execute(text(
            "SELECT m.*, ROUND(AVG(r.score), 2) AS average_score "
            "FROM movie m "
            "JOIN ratings r ON m.movieid = r.movie "
            "GROUP BY m.movieid "
            "ORDER BY average_score DESC "
            "LIMIT :top"
        ), {"top": top})
        return [dict(row._mapping) for row in result.fetchall()]
    
async def add_movie(title: str, year: int, genre: str, description: str, price: float):
    async with engine.connect() as conn:
        try:
            result = await conn.execute(text(
                "INSERT INTO movie (title, year, genre, description, price) "
                "VALUES (:title, :year, :genre, :description, :price) "
                "RETURNING movieid"
            ), {"title": title, "year": year, "genre": genre, "description": description, "price": price})        
            row = result.fetchone()
            await conn.commit()
            return row._mapping["movieid"] if row else None
        except IntegrityError:
            raise AlreadyExistsError("Movie already exists")
        
async def delete_movie(movieid: int):
    async with engine.connect() as conn:
        result = await conn.execute(text(
            "SELECT * FROM movie WHERE movieid = :movieid"
        ), {"movieid": movieid})
        movie = result.fetchone()
        if not movie:
            raise NotFoundError("Movie not found")
        
        await conn.execute(text(
            "DELETE FROM movie WHERE movieid = :movieid"
        ), {"movieid": movieid})
        await conn.commit()

async def rate_movie(userid: str, movieid: int, score: int, comment: str = None):
    async with engine.connect() as conn:
        result = await conn.execute(text(
            "SELECT * FROM movie WHERE movieid = :movieid"
        ), {"movieid": movieid})
        movie = result.fetchone()
        if not movie:
            raise NotFoundError("Movie not found")
        # Si hay excepcion aqui, SQLAlchemy devolvera error 500, y eso es correcto
        # Porque acamabos de ver que la pelicula existe y el usuario se verifica antes
        # Ademas score y comment son validados en la capa de servicio
        userid= await get_user_id(userid)
        await conn.execute(text(
            "INSERT INTO ratings (\"user\", movie, score, comment) "
            "VALUES (:userid, :movieid, :score, :comment) "
            "ON CONFLICT (\"user\", movie) DO UPDATE SET score = :score, comment = :comment"
        ), {"userid": userid, "movieid": movieid, "score": score, "comment": comment})
        await conn.commit()

async def delete_rating(userid: str, movieid: int):
    async with engine.connect() as conn:
        userid= await get_user_id(userid)
        result = await conn.execute(text(
            "DELETE FROM ratings WHERE \"user\" = :userid AND movie = :movieid"
        ), {"userid": userid, "movieid": movieid})
        await conn.commit()
        if result.rowcount == 0:
            raise NotFoundError("Rating not found")

async def get_actors(name):
    async with engine.connect() as conn:
        result = await conn.execute(text(
            "SELECT * FROM actor WHERE name = :name"
        ), {"name": name})
        return [dict(row._mapping) for row in result.fetchall()]

async def add_actor(name: str, birthdate):
    async with engine.connect() as conn:
        try:
            result = await conn.execute(text(
                "INSERT INTO actor (name, birthdate) "
                "VALUES (:name, :birthdate) "
                "RETURNING actorid"
            ), {"name": name, "birthdate": birthdate})        
            row = result.fetchone()
            await conn.commit()
            return row._mapping["actorid"] if row else None
        except IntegrityError:
            raise AlreadyExistsError("Actor already exists")

async def delete_actor(actorid: int):
    async with engine.connect() as conn:
        result = await conn.execute(text(
            "SELECT * FROM actor WHERE actorid = :actorid"
        ), {"actorid": actorid})
        actor = result.fetchone()
        if not actor:
            raise NotFoundError("Actor not found")
        
        await conn.execute(text(
            "DELETE FROM actor WHERE actorid = :actorid"
        ), {"actorid": actorid})
        await conn.commit()

async def add_actor_to_movie(movieid: int, actorid: int, character: str = None):
    async with engine.connect() as conn:
        result = await conn.execute(text(
            "SELECT * FROM movie WHERE movieid = :movieid"
        ), {"movieid": movieid})
        movie = result.fetchone()
        if not movie:
            raise NotFoundError("Movie not found")
        result = await conn.execute(text(
            "SELECT * FROM actor WHERE actorid = :actorid"
        ), {"actorid": actorid})
        actor = result.fetchone()
        if not actor:
            raise NotFoundError("Actor not found")
        try:
            await conn.execute(text(
                "INSERT INTO casts (movie,actor, character) "
                "VALUES (:movieid, :actorid, :character)"
            ), {"movieid": movieid, "actorid": actorid, "character": character})        
            await conn.commit()
        except IntegrityError:
            raise AlreadyExistsError("Character already exists in movie")
        
async def delete_actor_from_movie(movieid: int, actorid: int, character: str = None):
    async with engine.connect() as conn:
        result = await conn.execute(text(
            "DELETE FROM casts WHERE movie = :movieid AND actor = :actorid"
        ), {"movieid": movieid, "actorid": actorid})
        await conn.commit()
        if result.rowcount == 0:
            raise NotFoundError("Character not found in movie")

async def get_movie_by_id(movieid):
    async with engine.connect() as conn:
        result = await conn.execute(text(
            "SELECT * FROM movie WHERE movieid = :movieid"
        ), {"movieid": movieid})
        row = result.fetchone()
        return dict(row._mapping) if row else None

async def get_carts(user):
    async with engine.connect() as conn:
        user= await get_user_id(user)
        result = await conn.execute(text(
            "SELECT m.* FROM movie m "
            "JOIN carts_movies c ON  c.movie =m.movieid "
            "JOIN carts ON c.cart = carts.cartid "
            "WHERE carts.\"user\" = :user"
        ), {"user": user})
        return [dict(row._mapping) for row in result.fetchall()]

async def add_movie_to_cart(user, movieid):
    async with engine.connect() as conn:
        user= await get_user_id(user)
        cart= await conn.execute(text(
            "SELECT cartid FROM carts WHERE \"user\" = :user"
        ), {"user": user})
        cart=cart.fetchone()
        if not cart:
            raise NotFoundError("Cart not found")
        cartid=cart._mapping["cartid"]
        
        movie_in_cart= await conn.execute(text(
            "SELECT * FROM carts_movies WHERE cart = :cartid AND movie = :movieid"
        ), {"cartid": cartid, "movieid": movieid})
        movie_in_cart= movie_in_cart.fetchone()        
            
        if movie_in_cart:
            raise AlreadyExistsError("Movie already in cart")
        else:
            result = await conn.execute(text(
                "INSERT INTO carts_movies (cart, movie) VALUES (:cartid, :movieid)"
            ), {"cartid": cartid, "movieid": movieid})
            await conn.commit()

async def delete_movie_from_cart(user, movieid):
    async with engine.connect() as conn:
        # Obterner el ID del usuario y del carrito
        user= await get_user_id(user)
        cart = await conn.execute(text(
            "SELECT cartid FROM carts WHERE \"user\" = :user"
        ), {"user": user})
        cart=cart.fetchone()
        if not cart:
            raise NotFoundError("Cart not found")
        
        cartid=cart._mapping["cartid"]
        movie_in_cart= await conn.execute(text(
            "SELECT * FROM carts_movies WHERE cart = :cartid AND movie = :movieid"
        ), {"cartid": cartid, "movieid": movieid})
        movie_in_cart = movie_in_cart.fetchone()     
        if not cart:
            raise NotFoundError("Movie not found in cart")
        else:
            await conn.execute(text(
                "DELETE FROM carts_movies WHERE cart = :cartid AND movie = :movieid"
            ), {"cartid": cartid, "movieid": movieid})
            await conn.commit()

async def get_orders_by_userid(userid: str):
    async with engine.connect() as conn:
        userid= await get_user_id(userid)
        result = await conn.execute(text(
            "SELECT o.orderid, o.creationDate AS \"creationDate\",o.precio "
            "FROM \"order\" o "
            "WHERE o.\"user\" = :userid"
        ), {"userid": userid})
        orders = []
        for row in result.fetchall():
            order_details = {
                "orderid": row._mapping["orderid"],
                "date": row._mapping["creationDate"],
                "total": row._mapping["precio"],
                "user": {
                    "userid": user._mapping["userid"],
                    "name": user._mapping["name"],
                    "balance": float(user._mapping["balance"])
                },
                "movies": []
            }
            movies_result = await conn.execute(text(
                "SELECT m.movieid, m.title, m.year, m.genre, m.price "
                "FROM movie m "
                "JOIN orders_movies om ON m.movieid = om.movie "
                "WHERE om.\"order\" = :orderid"
            ), {"orderid": row._mapping["orderid"]})
            order_details["movies"] = [dict(movie_row._mapping) for movie_row in movies_result.fetchall()]
            orders.append(order_details)
        return orders
    
async def get_order_by_id(orderid: int):
    async with engine.connect() as conn:
        result = await conn.execute(text(
            "SELECT o.orderid, o.creationDate AS \"creationDate\",o.precio, u.userid, u.name, u.balance "
            "FROM \"order\" o "
            "JOIN \"user\" u ON o.\"user\" = u.userid "
            "WHERE o.orderid = :orderid"
        ), {"orderid": orderid})
        row = result.fetchone()
        
        if not row:
            return None
        
        order_details = {
                "orderid": row._mapping["orderid"],
                "date": row._mapping["creationDate"],
                "total": row._mapping["precio"],
                "user": {
                    "userid": row._mapping["userid"],
                    "name": row._mapping["name"],
                    "balance": float(row._mapping["balance"])
                },
                "movies": []
            }
        
        movies_result = await conn.execute(text(
            "SELECT m.movieid, m.title, m.year, m.genre, m.price "
            "FROM movie m "
            "JOIN orders_movies om ON m.movieid = om.movie "
            "WHERE om.\"order\" = :orderid"
        ), {"orderid": orderid})
        
        order_details["movies"] = [dict(mrow._mapping) for mrow in movies_result.fetchall()]
        
        return order_details
    
async def checkout_cart(user_uid):
    async with engine.connect() as conn:
        # Obtener el usuario y su ID en la BD
        user= await get_user_by_uid(user_uid)
        if not user:
            raise NotFoundError("User not found")
        user_id= user.get("userid")

        # Obtener el carrito del usuario y su ID
        cart= await conn.execute(text(
            "SELECT * FROM carts WHERE \"user\" = :user_id"
        ), {"user_id": user_id})
        cart=cart.fetchone()
        if not cart:
            raise NotFoundError("Cart not found")
        cartid=cart._mapping["cartid"]
        total_cost = cart._mapping["price"]
        
        
        result=await conn.execute(text(
            "INSERT INTO \"order\" (\"user\", creationDate, precio) VALUES (:user, :creationDate, :precio) RETURNING orderid"
        ), {"user": user_id, "creationDate": datetime.now(), "precio": total_cost})
        row= result.fetchone()
        

        await conn.commit()
        
        return dict(row._mapping) if row else None

