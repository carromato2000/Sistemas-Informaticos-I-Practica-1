-- Populate database with sample data

-- Películas
INSERT INTO peliculas (nombre, anio, genero, precio) VALUES 
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

-- Actores
INSERT INTO actores (nombre, fecha_nacimiento, fecha_defuncion) VALUES 
('Marlon Brando', '1924-04-03', '2004-07-01'),
('Al Pacino', '1940-04-25', NULL),
('John Travolta', '1954-02-18', NULL),
('Uma Thurman', '1970-04-29', NULL),
('Elijah Wood', '1981-01-28', NULL),
('Keanu Reeves', '1964-09-02', NULL),
('Carrie-Anne Moss', '1967-08-21', NULL),
('Leonardo DiCaprio', '1974-11-11', NULL),
('Kate Winslet', '1975-10-05', NULL),
('Matthew McConaughey', '1969-11-04', NULL),
('Anne Hathaway', '1982-11-12', NULL),
('Michael J. Fox', '1961-06-09', NULL),
('Ivana Baquero', '1994-06-11', NULL);

-- Repartos
INSERT INTO repartos (pelicula_id, actor_id, rol) VALUES 
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

-- Usuarios (usando UUIDs en formato hex de 32 caracteres)
INSERT INTO usuarios (id, nombre, contrasena, saldo) VALUES 
('a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6', 'usuario1', 'password123', 50.00),
('b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7', 'usuario2', 'securePass456', 75.50),
('c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8', 'usuario3', 'p@$$word789', 100.00),
('d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9', 'usuario4', 'safePassword', 30.25),
('e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0', 'usuario5', 'secretCode123', 60.75);

-- Valoraciones
INSERT INTO valoraciones (usuario, pelicula, nota, comentario) VALUES 
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

-- Carritos
INSERT INTO carritos (usuario, pelicula) VALUES 
('a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6', 2),
('a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6', 3),
('b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7', 4),
('c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8', 5),
('c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8', 6),
('d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9', 7),
('e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0', 8);

-- Pedidos
INSERT INTO pedidos (usuario, fecha, estado) VALUES 
('a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6', '2025-09-15 10:30:00', 'Completado'),
('b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7', '2025-09-20 14:45:00', 'Completado'),
('c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8', '2025-09-25 09:15:00', 'En proceso'),
('d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9', '2025-10-01 16:20:00', 'En proceso'),
('e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0', '2025-10-05 11:00:00', 'Pendiente');

-- Pedidos_Peliculas
INSERT INTO pedidos_peliculas (pedido, pelicula) VALUES 
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
