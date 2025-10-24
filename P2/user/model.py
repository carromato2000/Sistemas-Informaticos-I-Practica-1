import uuid
import bcrypt
import os
from sqlalchemy import select, and_, CHAR, Float, CheckConstraint, text, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.exc import IntegrityError
from exceptions import UserAlreadyExistsError, UserNotFoundError, InvalidCredentialsError

# Parametros de la base de datos
usuario= 'alumnodb'
contraseña= '1234'
host='db'
port= '5432'
database='si1'

# URL de la conexion
url_conexion=f'postgresql+asyncpg://{usuario}:{contraseña}@{host}:{port}/{database}'
engine=create_async_engine(url_conexion, echo=True)

Base = declarative_base()

class Usuario(Base):
    __tablename__='usuarios'
    __table_args__ = (
        CheckConstraint('saldo >= 0'),
    )

    id: Mapped[str]= mapped_column(CHAR(32),primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False, unique=True)
    contrasena: Mapped[str] = mapped_column(String(255),nullable=False)
    saldo: Mapped[float]= mapped_column(Float,nullable=False,default=0, server_default=text('0'))


    
async def create_user(name: str, password: str):
    async_session= sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    UID = uuid.uuid4()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    new_user = Usuario(
        id = UID.hex,
        nombre=name,
        contrasena=password_hash.decode('utf-8'),  # Decodificar bytes a string
    )
    
    async with async_session() as session:
        session.add(new_user)
        try:
            await session.commit()
            await session.refresh(new_user)  # Refrescar para obtener valores del servidor
        except IntegrityError:
            await session.rollback()
            raise UserAlreadyExistsError()
    
    return new_user

async def get_user(name: str, password: str):
    async_session= sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    async with async_session() as session:
        # Primero buscar el usuario por nombre
        result = await session.execute(
            select(Usuario).where(Usuario.nombre == name)
        )
        user = result.scalars().first()
        
        # Si existe, verificar la contraseña con bcrypt
    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user.contrasena.encode('utf-8')):
            return user
        else:
            raise (InvalidCredentialsError())
    else:
        raise (UserNotFoundError())
    