CREATE TABLE peliculas(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    anio INT NOT NULL,
    genero VARCHAR(255) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL CHECK (precio >= 0)
);

CREATE TABLE actores(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    fecha_defuncion DATE
    CHECK (fecha_defuncion IS NULL OR fecha_defuncion > fecha_nacimiento)
);

CREATE TABLE repartos(
    pelicula_id INT REFERENCES peliculas(id) ON DELETE CASCADE,
    actor_id INT REFERENCES actores(id) ON DELETE CASCADE,
    rol VARCHAR(255) NOT NULL
);

CREATE TABLE usuarios(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    saldo DECIMAL(10, 2) NOT NULL DEFAULT 0 CHECK (saldo >= 0)
);

CREATE TABLE valoraciones(
    usuario INT REFERENCES usuarios(id) ON DELETE CASCADE,
    pelicula INT REFERENCES peliculas(id) ON DELETE CASCADE,
    PRIMARY KEY (usuario, pelicula),
    nota INT NOT NULL,
    comentario TEXT
);

CREATE TABLE carritos(
    usuario INT REFERENCES usuarios(id) ON DELETE CASCADE,
    pelicula INT REFERENCES peliculas(id),
    PRIMARY KEY (usuario, pelicula)
);

CREATE TABLE pedidos(
    id SERIAL PRIMARY KEY,
    usuario INT REFERENCES usuarios(id) ON DELETE CASCADE,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(50) NOT NULL
);

CREATE TABLE pedidos_peliculas(
    pedido INT REFERENCES pedidos(id) ON DELETE CASCADE,
    pelicula INT REFERENCES peliculas(id),
    PRIMARY KEY (pedido, pelicula)
);