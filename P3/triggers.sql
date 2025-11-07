-- Trigger para actualizar el stock de películas al añadir/quitar del carrito
CREATE OR REPLACE FUNCTION actualizar_stock()
RETURNS trigger AS $$
BEGIN
    -- Si se añade una película al carrito, reducir stock en 1
    IF (TG_OP = 'INSERT') THEN
        UPDATE movie 
        SET stock = stock - 1
        WHERE movieid = NEW.movie;
        RETURN NEW;
    END IF;
    -- Si se quita una película del carrito, aumentar stock en 1
    IF (TG_OP = 'DELETE') THEN
        UPDATE movie 
        SET stock = stock + 1
        WHERE movieid = OLD.movie;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Crear el trigger
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
    END IF;
    -- Si se quita una película del carrito, reducir el precio del carrito
    IF (TG_OP = 'DELETE') THEN
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

CREATE OR REPLACE FUNCTION actualizar_balance_usuario()
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

CREATE TRIGGER trigger_actualizar_balance_usuario
AFTER INSERT ON "order"
FOR EACH ROW
EXECUTE FUNCTION actualizar_balance_usuario();

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


