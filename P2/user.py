from quart import Quart, jsonify, request

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker, AsyncSession
import json
import os
import uuid

usuario= 'alumnodb'
contraseña= '1234'
host='localhost'
port= '5432'
database='si1'
url_conexion=f'postgresql+asyncpg://{usuario}:{contraseña}@{host}:{port}/{database}'
engine=create_engine(url_conexion, echo=True)

Base= declarative_base()

class Usuario(Base):
    __tablename__='usuarios'
    id: Mapped[int]= mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(not_nullable=True)
    contrasena: Mapped[str] = mapped_column(not_nullable=True)
    saldo: Mapped[float]= mapped_column(not_nullable=True, default=0.0, checkable= 'saldo >= 0.0')

#secret_uuid=uuid.UUID(hex='00010203-0405-0607-0809-0a0b0c0d0e0f')
app = Quart(__name__)



@app.route('/user/create', methods=['POST'])

async def create_user():
    data=await request.get_json()
    name=data.get("name")
    if not name:
        return jsonify({"error": "Name data is empty"}), 404 

    elif not data.get("psswd"):
        return jsonify({"error": "Password data is empty"}), 404
    
    
    #UID=uuid.uuid4()
    #token=uuid.uuid5(secret_uuid,str(UID))
    
    async_session= sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    new_user =Usuario(
        nombre=name,
        contrasena=str(data.get("psswd")),
        saldo=data.get("saldo", 0.0)
    )
    
    async with async_session() as session:
        session.add(new_user)
        await session.commit()
    
    
    return jsonify(new_user)

@app.route('/user/login', methods=['POST'])
async def get_user():
    data = await request.get_json()
    name = data.get("name")
    psswd = data.get("psswd")
    if not name:
        return jsonify({"error": "Name data is empty"}), 404 

    elif not psswd:
        return jsonify({"error": "Password data is empty"}), 404
    
    async with async_session() as session:
        result = await session.execute(
            select(Usuario)
            .where(
                and_(
                    Usuario.nombre == name, 
                    Usuario.contrasena == psswd
                )
            )
        )
        user = result.scalars().first()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)


