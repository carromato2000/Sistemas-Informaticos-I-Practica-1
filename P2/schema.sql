CREATE TABLE movie(
    movieid SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    genre VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT
    CHECK (price >= 0)
);

CREATE TABLE actor(
    actorid SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE casts(
    movie INT REFERENCES movie(movieid) ON DELETE CASCADE,
    actor INT REFERENCES actor(actorid) ON DELETE CASCADE,
    character VARCHAR(255) NOT NULL
);

CREATE TABLE "user"(
    userid CHAR(32) PRIMARY KEY,    -- Usamos CHAR(32) porque guardaremos el UID haciendo UID.hex()
    name VARCHAR(255) NOT NULL UNIQUE, -- El nombre de usuario debe ser unico
    password VARCHAR(255) NOT NULL, -- Almacenaremos el hash de la contraseña
    balance REAL NOT NULL DEFAULT 0
    CHECK (balance >= 0)
);

CREATE TABLE ratings(
    "user" CHAR(32) REFERENCES "user"(userid) ON DELETE CASCADE,
    movie INT REFERENCES movie(movieid) ON DELETE CASCADE,
    PRIMARY KEY ("user", movie),
    score INT NOT NULL,
    comment TEXT
);

CREATE TABLE carts(
    "user" CHAR(32) REFERENCES "user"(userid) ON DELETE CASCADE,
    movie INT REFERENCES movie(movieid),
    PRIMARY KEY ("user", movie)
);

CREATE TABLE "order"(
    orderid SERIAL PRIMARY KEY,
    "user" CHAR(32) REFERENCES "user"(userid) ON DELETE CASCADE,
    creationDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    state VARCHAR(50) NOT NULL
);

CREATE TABLE orders_movies(
    "order" INT REFERENCES "order"(orderid) ON DELETE CASCADE,
    movie INT REFERENCES movie(movieid),
    PRIMARY KEY ("order", movie)
);