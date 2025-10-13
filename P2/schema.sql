CREATE TABLE peliculas(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    director VARCHAR(255) FOREIGN KEY REFERENCES directores(nombre),
    anio INT NOT NULL,
    genero VARCHAR(255) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL
)

CREATE TABLE directores(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    fecha_defuncion DATE
)

CREATE TABLE repartos(
    pelicula_id INT FOREIGN KEY REFERENCES peliculas(id),
    actor_id INT FOREIGN KEY REFERENCES actores(id),
    PRIMARY KEY (pelicula_id, actor_id),
    rol VARCHAR(255) NOT NULL
)

CREATE TABLE actores(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    fecha_defuncion DATE
)

CREATE TABLE usuarios(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    saldo DECIMAL(10, 2) NOT NULL
)

CREATE TABLE valoraciones(
    usuario INT FOREIGN KEY REFERENCES usuarios(id),
    pelicula INT FOREIGN KEY REFERENCES peliculas(id),
    PRIMARY KEY (usuario, pelicula),
    nota INT NOT NULL,
    comentario TEXT
)

CREATE TABLE carritos(
    usuario INT FOREIGN KEY REFERENCES usuarios(id),
    pelicula INT FOREIGN KEY REFERENCES peliculas(id),
    PRIMARY KEY (usuario, pelicula)
)
CREATE TABLE pedidos(
    id SERIAL PRIMARY KEY,
    usuario INT FOREIGN KEY REFERENCES usuarios(id),
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(50) NOT NULL
)

CREATE TABLE pedidos_peliculas(
    pedido INT FOREIGN KEY REFERENCES pedidos(id),
    pelicula INT FOREIGN KEY REFERENCES peliculas(id),
    PRIMARY KEY (pedido, pelicula)
)