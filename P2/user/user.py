from quart import Quart, jsonify, request

from sqlalchemy import select, and_
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import uuid
import os

# Parametros de la base de datos
usuario= 'alumnodb'
contraseña= '1234'
host='db'
port= '5432'
database='si1'

# URL de la conexion
url_conexion=f'postgresql+asyncpg://{usuario}:{contraseña}@{host}:{port}/{database}'
engine=create_async_engine(url_conexion, echo=True)

Base= declarative_base()

class Usuario(Base):
    __tablename__='usuarios'
    id: Mapped[int]= mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    contrasena: Mapped[str] = mapped_column(nullable=False)
    saldo: Mapped[float]= mapped_column(nullable=False,default=0.0)
    

#secret_uuid=uuid.UUID(hex='00010203-0405-0607-0809-0a0b0c0d0e0f')
app = Quart(__name__)

@app.route('/user', methods=['PUT'])

async def create_user():
    data=await request.get_json()
    name=data.get("name")
    if not name:
        return jsonify({"error": "Name data is empty"}), 404 

    elif not data.get("password"):
        return jsonify({"error": "Password data is empty"}), 404
    
    
    #UID=uuid.uuid4()
    #token=uuid.uuid5(secret_uuid,str(UID))
    
    async_session= sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    new_user =Usuario(
        nombre=name,
        contrasena=str(data.get("password")),
        saldo=data.get("saldo", 0.0)
    )
    
    async with async_session() as session:
        session.add(new_user)
        await session.commit()
    
    
    return jsonify(new_user)

@app.route('/user', methods=['GET'])
async def get_user():
    data = await request.get_json()
    name = data.get("name")
    password = data.get("password")
    async_session= sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    if not name:
        return jsonify({"error": "Name data is empty"}), 404 

    elif not password:
        return jsonify({"error": "Password data is empty"}), 404
    
    async with async_session() as session:
        result = await session.execute(
            select(Usuario)
            .where(
                and_(
                    Usuario.nombre == name, 
                    Usuario.contrasena == password
                )
            )
        )
        user = result.scalars().first()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)


