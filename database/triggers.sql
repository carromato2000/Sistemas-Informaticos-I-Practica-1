-- Trigger para actualizar el stock de películas al añadir/quitar del carrito
-- Función para validar el stock (BEFORE trigger)
CREATE OR REPLACE FUNCTION validate_stock()
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
CREATE OR REPLACE FUNCTION update_stock()
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
CREATE TRIGGER trigger_validate_stock
BEFORE INSERT ON carts_movies
FOR EACH ROW
EXECUTE FUNCTION validate_stock();

-- Trigger para actualizar el stock después de la operación
CREATE TRIGGER trigger_update_stock
AFTER INSERT OR DELETE ON carts_movies
FOR EACH ROW
EXECUTE FUNCTION update_stock();

CREATE OR REPLACE FUNCTION update_cart_price()
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
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_cart_price
AFTER INSERT OR DELETE ON carts_movies
FOR EACH ROW
EXECUTE FUNCTION update_cart_price();

CREATE OR REPLACE FUNCTION validate_user_balance()
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

CREATE OR REPLACE FUNCTION create_user_cart()
RETURNS trigger AS $$
BEGIN
    -- Al crear un usuario, crear su carrito asociado
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO carts ("user", price) VALUES (NEW.userid, 0);
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_create_user_cart
AFTER INSERT ON "user"
FOR EACH ROW
EXECUTE FUNCTION create_user_cart();

CREATE OR REPLACE FUNCTION update_user_balance()
RETURNS trigger AS $$
BEGIN
    -- Al crear una orden, reducir el balance del usuario
    IF (TG_OP = 'INSERT') THEN
        UPDATE "user"
        SET balance = balance - NEW.precio
        WHERE userid = NEW."user";
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validate_user_balance
BEFORE INSERT ON "order"
FOR EACH ROW
EXECUTE FUNCTION validate_user_balance();

CREATE TRIGGER trigger_update_user_balance
AFTER INSERT ON "order"
FOR EACH ROW
EXECUTE FUNCTION update_user_balance();

CREATE OR REPLACE FUNCTION clear_cart()
RETURNS trigger AS $$
DECLARE
    cartid INT;
BEGIN
    -- Al crear una orden, vaciar el carrito del usuario
    IF (TG_OP = 'INSERT') THEN
        SELECT c.cartid INTO cartid
        FROM carts c
        WHERE c."user" = NEW."user"
        LIMIT 1;
        BEGIN
            SET session_replication_role = 'replica';
            DELETE FROM carts_movies
            WHERE cart = cartid;
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

CREATE TRIGGER trigger_clear_cart
AFTER INSERT ON "order"
FOR EACH ROW
EXECUTE FUNCTION clear_cart();

CREATE OR REPLACE FUNCTION update_movie_rating()
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

CREATE TRIGGER trigger_update_movie_rating
AFTER INSERT OR UPDATE OR DELETE ON ratings
FOR EACH ROW
EXECUTE FUNCTION update_movie_rating();


