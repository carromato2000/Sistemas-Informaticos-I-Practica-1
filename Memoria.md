# Sistemas Informáticos I: Práctica I: Memoria

### Autores: Alfonso Briones Mediano y David Rodriguez Marrero

En esta práctica hemos desarrollado una aplicación distribuida basada en microservicios e implementada mediante una API Rest. Además hemos aprendido a desplegar estos microservicios en contenedores, usando para ello Docker.


## API

### Usuarios

La logica de este microservicio es muy sencilla. Hay dos rutas "/users/create" y "/users/login", a ambas se accede con el comando POST, y los datos del usuario (nombre y contraseña) han de ir en el cuerpo de la petición en formato JSON. 

Si se accede de este modo a cualquiera de estas rutas el servicio devolverá el id de usuario y el token de acceso o un codigo de error.

El codigo de error puede devolverse porque el usuario ya existiera, si se esta creando un usuario, o porque la contraseña no fuera correcta, si se esta iniciando sesión.

Los datos de los usuarios se guardan en users.txt, en cada linea de este archivo se guarda un usuario en formato JSON, que contiene su nombre "name", su contraseña "passwd" y su ID "id".

### Archivos

Las rutas de este microservicio son:
- /file/< UID >/< filename >: Si se eccede a esta ruta 


Los archivos de cada usuario se guardan en un directorio que tiene por nombre su ID de usuario. La primera linea de cada archivo indica si este es publico (1ª linea = "PUBLIC") o privado (1ª linea = "PRIVATE"), y el resto del archivo contiene lo que el usuario quiere guardar.

## Docker

En cuanto al apartado de docker, los ficheros y estructura utilizados son lo que cabría esperar de un trabajo de esas características. El archivo "docker-compose.yml" es muy simple y no hay nada de él que merezca mención. 

En cuanto a los Dockerfiles lo unico a destacar es el hecho de que para construir las imagenes, copiamos con "COPY . .", todo el contenido de las carpetas "user" y "file" en sus contenedores correspondientes, pero usando los .dockerignore para no copiar los propios Dockerfiles. 

Además tenemos en las dos carpetas el archivo requirements.txt, con las dependencias de cada microservicio, las cuales se instalan en los contenedores poniendo "RUN pip install -r requirements.txt" en los Dockerfiles.