-- Populate database with sample data

-- Movies
INSERT INTO movie (title, year, genre, price) VALUES 
('El Padrino', 1972, 'Drama', 9.99),
('Pulp Fiction', 1994, 'Thriller', 8.99),
('El Señor de los Anillos: La Comunidad del Anillo', 2001, 'Fantasía', 12.99),
('Matrix', 1999, 'Ciencia Ficción', 7.99),
('Titanic', 1997, 'Romance', 6.99),
('El Rey León', 1994, 'Animación', 5.99),
('Parásitos', 2019, 'Drama', 14.99),
('Interestelar', 2014, 'Ciencia Ficción', 11.99),
('Regreso al Futuro', 1985, 'Ciencia Ficción', 7.99),
('El Laberinto del Fauno', 2006, 'Fantasía', 9.99);

-- Actors
INSERT INTO actor (name) VALUES 
('Marlon Brando'),
('Al Pacino'),
('John Travolta'),
('Uma Thurman'),
('Elijah Wood'),
('Keanu Reeves'),
('Carrie-Anne Moss'),
('Leonardo DiCaprio'),
('Kate Winslet'),
('Matthew McConaughey'),
('Anne Hathaway'),
('Michael J. Fox'),
('Ivana Baquero');

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
(10, 13, 'Ofelia');

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
('e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0', 7, 5, 'Una película que rompe barreras'),
('e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0', 10, 4, 'Del Toro en su mejor momento');

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
INSERT INTO "order" ("user", creationDate, state) VALUES 
('a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6', '2025-09-15 10:30:00', 'Completado'),
('b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7', '2025-09-20 14:45:00', 'Completado'),
('c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8', '2025-09-25 09:15:00', 'En proceso'),
('d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9', '2025-10-01 16:20:00', 'En proceso'),
('e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0', '2025-10-05 11:00:00', 'Pendiente');

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
(5, 7),
(5, 10);
