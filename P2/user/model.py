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

class User(Base):
    __tablename__='user'
    __table_args__ = (
        CheckConstraint('saldo >= 0'),
    )

    userid: Mapped[str]= mapped_column(CHAR(32),primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255),nullable=False)
    balance: Mapped[float]= mapped_column(Float,nullable=False,default=0, server_default=text('0'))


    
async def create_user(name: str, password: str):
    async_session= sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    # Generar un UID único para el usuario y hashear la contraseña
    UID = uuid.uuid4()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Crear la instancia del usuario
    new_user = User(
        userid = UID.hex,
        name=name,
        password=password_hash.decode('utf-8'),  # Decodificar bytes a string
    )
    
    async with async_session() as session:
        session.add(new_user)
        try:
            await session.commit()
            await session.refresh(new_user)  # Refrescar para obtener valores del servidor
        except IntegrityError:
            await session.rollback()
            # Si hay un error de integridad, probablemente el usuario ya existe
            raise UserAlreadyExistsError()
    
    return new_user

async def get_user(name: str, password: str):
    async_session= sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    async with async_session() as session:
        # Primero buscar el usuario por nombre
        result = await session.execute(
            select(User).where(User.name == name)
        )
        user = result.scalars().first()
        
        # Si existe, verificar la contraseña con bcrypt
    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return user
        else:
            raise (InvalidCredentialsError())
    else:
        raise (UserNotFoundError())
    
async def delete_user(userid: str, calling_userid: str):
    async_session= sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    async with async_session() as session:
        # Comprobar si el usuario que llama es admin
        user_is_admin=await session.execute(
            select(User).where(and_(User.userid == calling_userid, User.name == 'admin'))
        )
        if not user_is_admin.scalars().first():
            raise PermissionError()
        
        if userid == calling_userid:
            raise PermissionError()
        
        # Obtener el usuario por userid
        result = await session.execute(
            select(User).where(User.userid == userid)
        )
        user = result.scalars().first()
        
        if not user:
            raise UserNotFoundError()
        
        # Eliminarlo
        await session.delete(user)
        await session.commit()
    
    return 0

async def update_password(userid: str, new_password: str):
    async_session= sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    async with async_session() as session:
        # Obtener el usuario por userid
        result = await session.execute(
            select(User).where(User.userid == userid)
        )
        user = result.scalars().first()
        
        if not user:
            raise UserNotFoundError()
        
        # Actualizar la contraseña
        new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        user.password = new_password_hash.decode('utf-8')
        
        # Guardar los cambios
        session.add(user)
        await session.commit()

async def update_credit(userid: str, amount:float):
    async_session= sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.userid == userid)
        )
        user = result.scalars().first()
        
        if not user:
            raise UserNotFoundError()
        
        user.balance += amount
        if user.balance < 0:
            raise ValueError("Insufficient balance")
        
        session.add(user)
        await session.commit()
        await session.refresh(user)
    
    return user