-- Populate database with sample data

-- Movies
INSERT INTO movie (title, year, genre, price, description) VALUES 
('El Padrino', 1972, 'Drama', 9.99, 'La historia de la familia Corleone, una de las más poderosas familias mafiosas de Nueva York.'),
('Pulp Fiction', 1994, 'Thriller', 8.99, 'Una serie de historias entrelazadas que giran en torno al crimen en Los Ángeles.'),
('El Señor de los Anillos: La Comunidad del Anillo', 2001, 'Fantasía', 12.99, 'Un hobbit llamado Frodo emprende un viaje para destruir un anillo poderoso.'),
('Matrix', 1999, 'Ciencia Ficción', 7.99, 'Un hacker descubre la verdadera naturaleza de su realidad y su papel en la guerra contra sus controladores.'),
('Titanic', 1997, 'Romance', 6.99, 'La trágica historia de amor entre Jack y Rose a bordo del fatídico RMS Titanic.'),
('El Rey León', 1994, 'Animación', 5.99, 'La aventura de un joven león llamado Simba que lucha por reclamar su lugar como rey.'),
('Parásitos', 2019, 'Drama', 14.99, 'Una familia pobre se infiltra en la vida de una familia rica, desencadenando una serie de eventos inesperados.'),
('Interestelar', 2014, 'Ciencia Ficción', 11.99, 'Un grupo de exploradores viaja a través de un agujero de gusano en el espacio en un intento por asegurar la supervivencia de la humanidad.'),
('Regreso al Futuro', 1985, 'Ciencia Ficción', 7.99, 'Un adolescente viaja en el tiempo y debe asegurarse de que sus padres se conozcan para no desaparecer.'),
('El Laberinto del Fauno', 2006, 'Fantasía', 9.99, 'Una joven se adentra en un mundo de fantasía para escapar de la realidad de la posguerra en España.'),
('Venom', 2018, 'Acción', 10.99, 'Un periodista se convierte en el huésped de un simbionte alienígena que le otorga superpoderes.'),
('Mad Max: Fury Road', 2015, 'Acción', 10.99 , 'Una mujer se rebela contra un gobernante tiránico en busca de su patria con la ayuda de un grupo de prisioneras');

-- Actors
INSERT INTO actor (name, birthdate) VALUES 
('Marlon Brando', '1924-04-03'),
('Al Pacino', '1940-04-25'),
('John Travolta', '1954-02-18'),
('Uma Thurman', '1970-04-29'),
('Elijah Wood', '1981-01-28'),
('Keanu Reeves', '1964-09-02'),
('Carrie-Anne Moss', '1967-08-21'),
('Leonardo DiCaprio', '1974-11-11'),
('Kate Winslet', '1975-10-05'),
('Matthew McConaughey', '1969-11-04'),
('Anne Hathaway', '1982-11-12'),
('Michael J. Fox', '1961-06-09'),
('Ivana Baquero', '1994-06-11'),
('Tom Hardy', '1977-09-15');

-- Casts
INSERT INTO casts (movie, actor, character) VALUES 
(1, 1, 'Don Vito Corleone'),
(1, 2, 'Michael Corleone'),
(2, 3, 'Vincent Vega'),
(2, 4, 'Mia Wallace'),
(3, 5, 'Frodo Bolsón'),
(4, 6, 'Neo'),
(4, 7, 'Trinity'),
(5, 8, 'Jack Dawson'),
(5, 9, 'Rose DeWitt Bukater'),
(8, 10, 'Joseph Cooper'),
(8, 11, 'Dra. Amelia Brand'),
(9, 12, 'Marty McFly'),
(10, 13, 'Ofelia'),
(11, 14, 'Eddie Brock'),
(12, 14, 'Max Rockatansky');

-- Users (using bcrypt hashed passwords)

--usuario1: password123
--usuario2: securePass456
--usuario3: p@$$word789
--usuario4: safePassword
--usuario5: secretCode123
--admin: admin
INSERT INTO "user" (userid, name, password, balance) VALUES 
('a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6', 'usuario1', '$2b$12$wvaPF93z53ByVUtgIyOkf.Se6wgbmoO7g7CtKCW1haThka1.Y51qi', 50.00),
('b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7', 'usuario2', '$2b$12$YYj0hAAJLXIPuKR//tWHZOO5cZ9uC4Z7VAJMLofZTFaiD7JUqq/2C', 75.50),
('c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8', 'usuario3', '$2b$12$XDPo9HUfvAjzodqxdZ7hy.5PE0Cm4iiGQ9FTquRQ1Bw7a8AuSxwxi', 100.00),
('d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9', 'usuario4', '$2b$12$Twb/9rlaK5UJMHFcO2QO8eQtU7mqt3CRTUOPcfy8mnvrTZpObgdue', 30.25),
('e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0', 'usuario5', '$2b$12$bY5rSSuQPUZz8bV3pKn0b.HKiSFmljLWYTuJqrD7.0ITvRCdCnFZS', 60.75),
('f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1', 'admin', '$2b$12$FrRVXK7qp5K2k2tSTpWXdeIUgyVx3CXkcsA8wvr4vjJTTkmgWqTES', 999.99);

-- Ratings
INSERT INTO ratings ("user", movie, score, comment) VALUES 
('a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6', 1, 5, 'Una obra maestra del cine'),
('a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6', 4, 4, 'Revolucionaria para su época'),
('b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7', 2, 5, 'Excelente dirección de Tarantino'),
('b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7', 5, 3, 'Buena historia pero algo lenta'),
('c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8', 3, 5, 'Increíble adaptación de Tolkien'),
('c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8', 8, 5, 'Una experiencia visual impresionante'),
('d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9', 9, 4, 'Un clásico de ciencia ficción'),
('d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9', 6, 5, 'La mejor película de Disney'),
('d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9', 12, 5, 'La mejor película película de acción'),
('e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0', 7, 5, 'Una película que rompe barreras'),
('e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0', 10, 4, 'Del Toro en su mejor momento'),
('e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0', 11, 3, 'Entretenida pero predecible');


-- Carts
INSERT INTO carts ("user", movie) VALUES 
('a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6', 2),
('a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6', 3),
('b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7', 4),
('c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8', 5),
('c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8', 6),
('d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9', 7),
('e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0', 8);

-- Orders
INSERT INTO "order" ("user", creationDate, state, precio) VALUES 
('a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6', '2025-09-15 10:30:00', 'Completado', 18.98),
('b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7', '2025-09-20 14:45:00', 'Completado', 16.98),
('c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8', '2025-09-25 09:15:00', 'En proceso', 24.98),
('d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9', '2025-10-01 16:20:00', 'En proceso', 15.98),
('e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0', '2025-10-05 11:00:00', 'Pendiente', 30.97);

-- Orders_Movies
INSERT INTO orders_movies ("order", movie) VALUES 
(1, 1),
(1, 4),
(2, 2),
(2, 5),
(3, 3),
(3, 8),
(4, 9),
(4, 6),
(4, 12),
(5, 7),
(5, 10),
(5, 11);
