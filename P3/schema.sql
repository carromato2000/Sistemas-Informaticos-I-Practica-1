CREATE TABLE movie(
    movieid SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    genre VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    description TEXT,
    UNIQUE(title, year)
);

CREATE TABLE actor(
    actorid SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthdate DATE,
    UNIQUE(name, birthdate)
);

CREATE TABLE casts(
    movie INT REFERENCES movie(movieid) ON DELETE CASCADE,
    actor INT REFERENCES actor(actorid) ON DELETE CASCADE,
    character VARCHAR(255) NOT NULL,
    PRIMARY KEY (movie, actor, character)
);

CREATE TABLE "user"(
    userid SERIAL PRIMARY KEY,
    apiid CHAR(32) NOT NULL UNIQUE,    -- Usamos CHAR(32) porque guardaremos el UID haciendo UID.hex()
    name VARCHAR(255) NOT NULL UNIQUE, -- El nombre de usuario debe ser unico
    password VARCHAR(255) NOT NULL, -- Almacenaremos el hash de la contraseña
    balance DECIMAL(10,2) NOT NULL DEFAULT 0
    CHECK (balance >= 0)
);

CREATE TABLE ratings(
    "user" INT REFERENCES "user"(userid) ON DELETE CASCADE,
    movie INT REFERENCES movie(movieid) ON DELETE CASCADE,
    PRIMARY KEY ("user", movie),
    score INT NOT NULL,
    comment TEXT
);

CREATE TABLE carts(
    cartid SERIAL PRIMARY KEY,
    "user" INT REFERENCES "user"(userid) ON DELETE CASCADE
);

CREATE TABLE carts_movies(
    cart INT REFERENCES carts(cartid) ON DELETE CASCADE,
    movie INT REFERENCES movie(movieid) ON DELETE CASCADE,
    PRIMARY KEY (cart, movie)
);

CREATE TABLE "order"(
    orderid SERIAL PRIMARY KEY,
    "user" INT REFERENCES "user"(userid) ON DELETE CASCADE,
    creationDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    precio DECIMAL(10,2) NOT NULL DEFAULT 0
);

CREATE TABLE orders_movies(
    "order" INT REFERENCES "order"(orderid) ON DELETE CASCADE,
    movie INT REFERENCES movie(movieid),
    PRIMARY KEY ("order", movie)
);