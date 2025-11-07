-- Trigger para actualizar el stock de películas al añadir/quitar del carrito
-- Función para validar el stock (BEFORE trigger)
CREATE OR REPLACE FUNCTION validar_stock()
RETURNS trigger AS $$
    DECLARE movie_stock INT;
BEGIN
    -- Solo validamos en INSERT
    IF (TG_OP = 'INSERT') THEN
        SELECT stock INTO movie_stock
        FROM movie
        WHERE movieid = NEW.movie;
        
        IF (movie_stock <= 0) THEN
            RAISE EXCEPTION 'No hay suficiente stock para la película con ID %', NEW.movie;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Función para actualizar el stock (AFTER trigger)
CREATE OR REPLACE FUNCTION actualizar_stock()
RETURNS trigger AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        UPDATE movie
        SET stock = stock - 1
        WHERE movieid = NEW.movie;
    ELSIF (TG_OP = 'DELETE') THEN
        UPDATE movie 
        SET stock = stock + 1
        WHERE movieid = OLD.movie;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Trigger para validar el stock antes de insertar
CREATE TRIGGER trigger_validar_stock
BEFORE INSERT ON carts_movies
FOR EACH ROW
EXECUTE FUNCTION validar_stock();

-- Trigger para actualizar el stock después de la operación
CREATE TRIGGER trigger_actualizar_stock
AFTER INSERT OR DELETE ON carts_movies
FOR EACH ROW
EXECUTE FUNCTION actualizar_stock();

CREATE OR REPLACE FUNCTION actualizar_precio_carrito()
RETURNS trigger AS $$
BEGIN
    -- Si se añade una película al carrito, aumentar el precio del carrito
    IF (TG_OP = 'INSERT') THEN
        UPDATE carts
        SET price = price + (SELECT price FROM movie WHERE movieid = NEW.movie)
        WHERE cartid = NEW.cart;
        RETURN NEW;
    -- Si se quita una película del carrito, reducir el precio del carrito
    ELSIF (TG_OP = 'DELETE') THEN
        UPDATE carts
        SET price = price - (SELECT price FROM movie WHERE movieid = OLD.movie)
        WHERE cartid = OLD.cart;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;

CREATE TRIGGER trigger_actualizar_precio_carrito
AFTER INSERT OR DELETE ON carts_movies
FOR EACH ROW
EXECUTE FUNCTION actualizar_precio_carrito();

CREATE OR REPLACE FUNCTION validar_balance_usuario()
RETURNS trigger AS $$
DECLARE user_balance DECIMAL(10,2);
BEGIN
    -- Al crear una orden, validar que el usuario tiene suficiente balance
    IF (TG_OP = 'INSERT') THEN
        SELECT balance INTO user_balance
        FROM "user"
        WHERE userid = NEW."user";
        IF (user_balance < NEW.precio) THEN
            RAISE EXCEPTION 'El usuario con ID % no tiene suficiente balance para realizar la orden', NEW."user";
        END IF;
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION actualizar_balance_usuario()
RETURNS trigger AS $$
BEGIN
    -- Al crear una orden, reducir el balance del usuario
    IF (TG_OP = 'INSERT') THEN
        UPDATE "user"
        IF balance < NEW.precio

        WHERE userid = NEW."user";
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_balance_usuario
BEFORE INSERT ON "order"
FOR EACH ROW
EXECUTE FUNCTION validar_balance_usuario();

CREATE TRIGGER trigger_actualizar_balance_usuario
AFTER INSERT ON "order"
FOR EACH ROW
EXECUTE FUNCTION actualizar_balance_usuario();

CREATE OR REPLACE FUNCTION limpar_carrito()
RETURNS trigger AS $$
BEGIN
    -- Al crear una orden, vaciar el carrito del usuario
    IF (TG_OP = 'INSERT') THEN
        BEGIN
            SET session_replication_role = 'replica';
            DELETE FROM carts_movies
            WHERE cart = (SELECT cartid FROM carts WHERE "user" = NEW."user");
            UPDATE carts
            SET price = 0
            WHERE "user" = NEW."user";
            SET session_replication_role = 'origin';
            RETURN NEW;
        EXCEPTION WHEN OTHERS THEN
            SET session_replication_role = 'origin';
            RAISE;
        END;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_limpar_carrito
AFTER INSERT ON "order"
FOR EACH ROW
EXECUTE FUNCTION limpar_carrito();

CREATE OR REPLACE FUNCTION actualizar_rating_pelicula()
RETURNS trigger AS $$
DECLARE
    nueva_media DECIMAL(2,1);
BEGIN
    -- Calcular la nueva media de puntuaciones para la película afectada
    IF (TG_OP = 'INSERT' OR TG_OP = 'UPDATE') THEN
        SELECT AVG(score) INTO nueva_media
        FROM ratings
        WHERE movie = NEW.movie;
        UPDATE movie
        SET rating = ROUND(nueva_media::numeric, 1)
        WHERE movieid = NEW.movie;
        RETURN NEW;
    END IF;
    IF (TG_OP = 'DELETE') THEN
        SELECT AVG(score) INTO nueva_media
        FROM ratings
        WHERE movie = OLD.movie;
        UPDATE movie
        SET rating = ROUND(nueva_media::numeric, 1)
        WHERE movieid = OLD.movie;
        RETURN OLD;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_actualizar_rating_pelicula
AFTER INSERT OR UPDATE OR DELETE ON ratings
FOR EACH ROW
EXECUTE FUNCTION actualizar_rating_pelicula();


