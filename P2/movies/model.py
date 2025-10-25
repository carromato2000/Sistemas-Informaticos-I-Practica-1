from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import text
from datetime import datetime


usuario= 'alumnodb'
contraseña= '1234'
host='db'
port= '5432'
database='si1'

url_conexion=f'postgresql+asyncpg://{usuario}:{contraseña}@{host}:{port}/{database}'
engine=create_async_engine(url_conexion, echo=True)

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

async def get_movie_by_id(movieid):
    async with engine.connect() as conn:
        result = await conn.execute(text(
            "SELECT * FROM movie WHERE movieid = :movieid"
        ), {"movieid": movieid})
        row = result.fetchone()
        return dict(row._mapping) if row else None

async def get_carts(user):
    async with engine.connect() as conn:
        
        result = await conn.execute(text(
            "SELECT m.* FROM movie m "
            "JOIN carts c ON m.movieid = c.movie "
            "WHERE c.\"user\" = :user"
        ), {"user": user})
        return [dict(row._mapping) for row in result.fetchall()]

async def add_movie_to_cart(user, movieid):
    if movieid is None:
        return False
    async with engine.connect() as conn:
        cart_check= await conn.execute(text(
            "SELECT * FROM carts WHERE \"user\" = :user AND movie = :movieid"
        ), {"user": user, "movieid": movieid})
        cart=[dict(row._mapping) for row in cart_check.fetchall()]
        if cart:
            return False
        else:
            await conn.execute(text(
                "INSERT INTO carts (\"user\", movie) VALUES (:user, :movieid)"
            ), {"user": user, "movieid": movieid})
            await conn.commit()
            return True

async def delete_movie_from_cart(user, movieid):
    async with engine.connect() as conn:
        movie_in_cart= await conn.execute(text(
            "SELECT * FROM carts WHERE \"user\" = :user AND movie = :movieid"
        ), {"user": user, "movieid": movieid})
        if not movie_in_cart.fetchone():
            return False
        else:
            await conn.execute(text(
                "DELETE FROM carts WHERE \"user\" = :user AND movie = :movieid"
            ), {"user": user, "movieid": movieid})
            await conn.commit()
            return True
        

async def update_credit(userid: str, amount: float):
    async with engine.connect() as conn:
        result = await conn.execute(text(
            "SELECT * FROM \"user\" WHERE userid = :userid"
        ), {"userid": userid})
        user = result.fetchone()
        
        if not user:
            return -1
        
        new_balance = user.balance + amount
        
        await conn.execute(text(
            "UPDATE \"user\" SET balance = :balance WHERE userid = :userid"
        ), {"balance": new_balance, "userid": userid})
        await conn.commit()
        
        return new_balance
    
async def get_order_by_id(orderid: int):
    async with engine.connect() as conn:
        result = await conn.execute(text(
            "SELECT o.orderid, o.creationDate AS \"creationDate\", o.state,o.precio, u.userid, u.name, u.balance "
            "FROM \"order\" o "
            "JOIN \"user\" u ON o.\"user\" = u.userid "
            "WHERE o.orderid = :orderid"
        ), {"orderid": orderid})
        order_row = result.fetchone()
        
        if not order_row:
            return None
        
        order_details = {
            "orderid": order_row.orderid,
            "date": order_row.creationDate,
            "state": order_row.state,
            "total": order_row.precio,
            "user": {
                "userid": order_row.userid,
                "name": order_row.name,
                "balance": float(order_row.balance)
            },
            "movies": []
        }
        
        movies_result = await conn.execute(text(
            "SELECT m.movieid, m.title, m.year, m.genre, m.price "
            "FROM movie m "
            "JOIN orders_movies om ON m.movieid = om.movie "
            "WHERE om.\"order\" = :orderid"
        ), {"orderid": orderid})
        
        order_details["movies"] = [dict(row._mapping) for row in movies_result.fetchall()]
        
        return order_details
    
async def checkout_cart(user_id):
    async with engine.connect() as conn:
        result = await conn.execute(text(
            "SELECT * FROM \"user\" WHERE userid = :userid"
        ), {"userid": user_id})
        user = result.fetchone()
        
        if not user:
            return -1
        
        cart_result = await conn.execute(text(
            "SELECT m.* FROM movie m "
            "JOIN carts c ON m.movieid = c.movie "
            "WHERE c.\"user\" = :user"
        ), {"user": user_id})
        cart_items = [dict(row._mapping) for row in cart_result.fetchall()]
        
        if not cart_items:
            return -2
        
        total_cost = sum(item['price'] for item in cart_items)
        
        if user.balance < total_cost:
            return -3
        
        new_balance = float(user.balance) - float(total_cost)
        
        await conn.execute(text(
            "UPDATE \"user\" SET balance = :balance WHERE userid = :userid"
        ), {"balance": new_balance, "userid": user_id})
        
        
        result=await conn.execute(text(
            "INSERT INTO \"order\" (\"user\", creationDate, state, precio) VALUES (:user, :creationDate,:state, :precio) RETURNING orderid"
        ), {"user": user_id, "creationDate": datetime.now(), "state": "Pendiente", "precio": total_cost})
        row= result.fetchone()
        
        
        for item in cart_items:
            await conn.execute(text(
                "INSERT INTO orders_movies (\"order\", movie) "
                "VALUES (:orderid, :movieid)"
            ), {"orderid": row._mapping["orderid"], "movieid": item["movieid"]})
        
        await conn.execute(text(
            "DELETE FROM carts WHERE \"user\" = :user"
        ), {"user": user_id})
        
        await conn.commit()
        
        return dict(row._mapping) if row else None
    
async def set_credit(userid: str, amount: float):
    async with engine.connect() as conn:
        result = await conn.execute(text(
            "SELECT * FROM \"user\" WHERE userid = :userid"
        ), {"userid": userid})
        user = result.fetchone()
        
        if not user:
            return -1
        
        await conn.execute(text(
            "UPDATE \"user\" SET balance = :balance WHERE userid = :userid"
        ), {"balance": amount, "userid": userid})
        await conn.commit()
        
        return amount
