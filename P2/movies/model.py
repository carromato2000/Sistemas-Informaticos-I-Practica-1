from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import text

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

