CREATE OR REPLACE FUNCTION get_user_by_apiid(p_apiid CHAR(32))
    RETURNS TABLE(userid INTEGER, name VARCHAR, balance REAL, nationality VARCHAR, discount INT) AS $$
    BEGIN
        RETURN QUERY
        SELECT u.userid, u.name, u.balance, u.nationality, u.discount
        FROM "user" u
        WHERE u.apiid = p_apiid;
        
        IF NOT FOUND THEN
            -- Opcionalmente, podrías lanzar una excepción si no se encuentra el usuario
            -- RAISE EXCEPTION 'User with apiid % not found', p_apiid;
            RETURN;
        END IF;
    END;
    $$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE checkout_cart(userid INT)
    AS $$
    DECLARE 
        discount INT;
        total_price DECIMAL(10,2);
        user_balance DECIMAL(10,2);
    BEGIN
        -- Lógica para procesar el checkout del carrito del usuario
        -- Esta función puede incluir la creación de una orden, actualización de stock, etc.
        -- Por simplicidad, aquí solo se muestra un mensaje
        SELECT u.discount, u.balance INTO discount
        FROM "user" u
        WHERE u.userid = userid;

        IF NOT FOUND THEN
            RAISE EXCEPTION 'User with ID % not found', userid;
        END IF;

        SELECT c.price INTO total_price
        FROM carts c
        WHERE c."user" = userid;

        IF NOT FOUND OR total_price IS NULL THEN
            RAISE EXCEPTION 'Cart is empty for user %', userid;
        END IF;


        total_price := total_price * (1 - discount / 100.0);

        IF user_balance < total_price THEN
            RAISE EXCEPTION 'Insufficient balance for user %', userid;
        END IF;

        -- Los triggers se encargarán de actualizar el balance del usuario y limpiar el carrito
        INSERT INTO orders ("user", creationDate, precio) VALUES (userid, CURRENT_TIMESTAMP, total_price); 
    END;
    $$ LANGUAGE plpgsql;
