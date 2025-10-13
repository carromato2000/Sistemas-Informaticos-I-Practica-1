# Sistemas Informáticos I: Práctica I: Memoria

### Autores: Alfonso Briones Mediano y David Rodriguez Marrero

En esta práctica hemos desarrollado una aplicación distribuida basada en microservicios e implementada mediante una *API Rest*.
Además, hemos aprendido a desplegar estos microservicios en contenedores, usando para ello *Docker*.


## API

### Usuarios

La lógica de este microservicio es muy sencilla. Hay dos rutas */users/create* y */users/login*, a ambas se accede con el comando *POST*, y los datos del usuario (nombre y contraseña) han de ir en el cuerpo de la petición en formato *JSON*. 

Si se accede de este modo a cualquiera de estas rutas el servicio devolverá el id de usuario y el token de acceso, o un mensaje de error.

El mensaje de error puede devolverse porque se intente crear un usuario que ya exista, porque la contraseña no fuera correcta al iniciar sesión, o porque el usuario o contraseña fueran una cadena vacía.

Los datos de los usuarios se guardan en *users.txt*, en cada linea de este archivo se guarda un usuario en formato *JSON*, que contiene su nombre "name", su contraseña *passwd* y su ID *id*.

### Archivos

El token de acceso de los usuarios, se pasa en la cabecera de las peticiones http, de esta manera podemos pasar el token en peticiones *GET* (las cuales no tienen cuerpo). Las únicas peticiones que no verifican el token de acceso son las peticiones GET a archivos públicos y las peticioens *GET* a archivos que han sido compartidos.

Las opciones de este microservicio son:
- **PUT.../file/UID/filename**: El cuerpo de la petición debe de contener un diccionario con la forma *{'public':bool, 'content':str}*. Si el token es válido se crea el archivo y se devuelve un mensaje de éxito. En otro caso se devuelve un mensaje de error.
- **GET.../file/UID/filename**: Si el archivo existe y, el token es válido o el archivo es público, se devuelve el contenido del archivo. En otro caso de devuelve un mensaje de error.
- **DELETE.../file/UID/filename**: Si el token es válido y el archivo existe, se elimina el archivo y se devuelve un mensaje de éxito. En otro caso se devuelve un mensaje de error.
- **GET/file/UID**: Si el token es válido se devuelve el listado de los archivos del usuario. En otro caso se devuelve un mensaje de error.
- **POST.../file/UID/filename/share**: Si el token es válido se genera un share_token para compartir el archivo con otros usuarios.
- **GET.../share/share_token**: Si el share_token es válido, se devuelve el contenido del archivo al que se refiere. En otro caso se devuelve un mensaje de error.


Los archivos de cada usuario se guardan en un directorio que tiene por nombre su ID de usuario. La primera linea de cada archivo indica si este es público (1ª linea = "PUBLIC") o privado (1ª linea = "PRIVATE"), y el resto del archivo contiene lo que el usuario quiere guardar.

## Docker

En cuanto al apartado de docker, los ficheros y estructura utilizados son lo que cabría esperar de un trabajo de esas características. El archivo "docker-compose.yml" es muy simple y no hay nada de él que merezca mención. 

En cuanto a los *Dockerfiles* lo unico a destacar es el hecho de que para construir las imagenes, copiamos con *COPY . .*, todo el contenido de las carpetas *user* y *file* en sus contenedores correspondientes, pero usando los *.dockerignore* para no copiar los propios *Dockerfiles*. 

Además tenemos en las dos carpetas el archivo *requirements.txt* que contiene la salida de *pip freeze* sobre nuestro entorno virtual de python usado durante el desarrollo.

Para desplegar los servicios ejecutamos *sudo docker-compose up --build -d*. Con la opción *--build* reconstruimos las imagenes para aplicar los cambios y con *-d* hacemos que los contenedores se ejecuten sin bloquear la terminal.
