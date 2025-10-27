
import requests
from http import HTTPStatus
import cliente_users

from urls import USERS, CATALOG, ok

test_failed = 0
test_passed = 0

def main(headers_alice, headers_admin):
    print("# =======================================================")
    print("# Distintas consultas de alice al catálogo de películas")
    print("# =======================================================")

    r = requests.get(f"{CATALOG}/movies", headers=headers_alice)
    if ok("Obtener catálogo de películas completo", r.status_code == HTTPStatus.OK):
        data = r.json()
        if data:
            for movie in data:
                print(f"\t- {movie['title']}\n\t  {movie['description']}")
        else:
            print("\tNo hay películas en el catálogo")
    movieids = []
    # Se asume que al menos hay una película que cumple la condición. Si no se reciben
    # los datos de ninguna película el test se da por no satisfecho
    r = requests.get(f"{CATALOG}/movies", params={"title": "Matrix"}, headers=headers_alice)
    if ok("Buscar películas con 'Matrix' en el título", r.status_code == HTTPStatus.OK and r.json()):
        data = r.json()
        if data:
            for movie in data:
                print(f"\t[{movie['movieid']}] {movie['title']}")
                movieids.append(movie['movieid'])

    r = requests.get(f"{CATALOG}/movies", params={"title": "No debe haber pelis con este título"}, headers=headers_alice)
    ok("Búsqueda fallida de películas por título", r.status_code == HTTPStatus.OK and not r.json())

    r = requests.get(f"{CATALOG}/movies", params={"title": ""}, headers=headers_alice)
    ok("Búsqueda de películas con título vacío:", r.status_code == HTTPStatus.OK and not r.json())

    r = requests.put(f"{CATALOG}/movies", params={"title": "Nueva Película", "year": 2024, "genre": "Drama", "price" : 9.99},
                     data ={"description": "Descripción de la nueva película"}, headers=headers_alice)
    if ok("Intento de añadir película por usuario no admin", r.status_code == HTTPStatus.UNAUTHORIZED):
        pass
    else:
        print(r.status_code, r.text)

    movie_id = ""
    r = requests.put(f"{CATALOG}/movies", params={"title": "Fight Club", "year": 1999, "genre": "Drama", "price" : 7.99},
                     data ={"description": "...",}, headers=headers_admin)
    if ok("Añadir película por usuario admin", r.status_code == HTTPStatus.CREATED and r.json()):
        data = r.json()
        movie_id = data["movieid"]
    else:
        print(r.status_code, r.text)

    r = requests.put(f"{CATALOG}/movies", params={"title": "Fight Club", "year": 1999, "genre": "Drama", "price" : 7.99},
                    data ={"description": "...",}, headers=headers_admin)
    if ok("Intento de añadir película ya existente", r.status_code == HTTPStatus.CONFLICT):
        pass
    else:
        print(r.status_code, r.text)

    r = requests.get(f"{CATALOG}/movies",params={'title': 'Fight Club'}, headers=headers_admin)
    if ok("Verificar que la película añadida existe", r.status_code == HTTPStatus.OK and r.json()):
        data = r.json()
        if movie_id != data[0]['movieid']:
            print(f"Error: El ID de la película añadida no coincide: {movie_id} != {data[0]['movieid']}")
        else:
            print(f"\tID de la nueva película: {movie_id}")
        movie_id = data[0]['movieid']

    r = requests.delete(f"{CATALOG}/movies/{movie_id}", headers=headers_alice)
    if ok("Intento de eliminar película por usuario no admin", r.status_code == HTTPStatus.UNAUTHORIZED):
        pass
    else:
        print(r.status_code, r.text)

    r = requests.delete(f"{CATALOG}/movies/{movie_id}", headers=headers_admin)
    if ok("Eliminar película por usuario admin", r.status_code == HTTPStatus.OK):
        pass
    else:
        print(r.status_code, r.text)

    r = requests.delete(f"{CATALOG}/movies/hola", headers=headers_admin)
    if ok("Intento de eliminar película con ID no numérico", r.status_code == HTTPStatus.BAD_REQUEST):
        pass
    else:
        print(r.status_code, r.text)

    r = requests.delete(f"{CATALOG}/movies/99999999", headers=headers_admin)
    if ok("Intento de eliminar película inexistente", r.status_code == HTTPStatus.NOT_FOUND):
        pass
    else:
        print(r.status_code, r.text)

    # Los ids de estas búsqueda se utilizarán después para las pruebas de la gestión
    # del carrito
    
    r = requests.get(f"{CATALOG}/movies", params={"title": "Gladiator", "year": 2000, "genre": "action"}, headers=headers_alice)
    if ok("Buscar películas por varios campos de movie", r.status_code == HTTPStatus.OK):
        data = r.json()
        if data:
            for movie in data:
                print(f"\t[{movie['movieid']}] {movie['title']}")
                movieids.append(movie['movieid'])
            
            r = requests.get(f"{CATALOG}/movies/{movieids[0]}", headers=headers_alice)
            if ok(f"Obtener detalles de la película con ID [{movieids[0]}]", 
                  r.status_code == HTTPStatus.OK and r.json() and r.json()['movieid'] == movieids[0]):
                data = r.json()
                print(f"\t{data['title']} ({data['year']})")
                print(f"\tGénero: {movie['genre']}")
                print(f"\tDescripción: {movie['description']}")
                print(f"\tPrecio: {movie['price']}")
        else:
            print("\tNo se encontraron películas.")
    
    r = requests.get(f"{CATALOG}/movies/99999999", headers=headers_alice)
    ok(f"Obtener detalles de la película con ID no válido", HTTPStatus.NOT_FOUND)
    
    ## Prueba de david id
    r= requests.get(f"{CATALOG}/movies/11", headers=headers_alice)
    ok(f"Obtener detalles de la película con ID 11", r.status_code == HTTPStatus.OK and r.json() and r.json()['movieid'] == 11)
    data = r.json()
    print(f"\tTitulo: {data['title']}") 
    print(f"\tAño: {data['year']}")
    print(f"\tGénero: {data['genre']}")
    print(f"\tDescripción: {data['description']}")
    print(f"\tPrecio: {data['price']}")
    
    r = requests.get(f"{CATALOG}/movies", params={"actor": "Tom Hardy"}, headers=headers_alice)
    if ok("Buscar películas en las que participa 'Tom Hardy'", r.status_code == HTTPStatus.OK and r.json()):
        data = r.json()
        if data:
            for movie in data:
                print(f"\t[{movie['movieid']}] {movie['title']}")
                movieids.append(movie['movieid'])

    r = requests.put(f"{CATALOG}/actors", params={"name": "Chris Hemsworth", "birthdate": "1977-09-15"},
                     headers=headers_alice)
    if ok("Intento de añadir actor por usuario no admin", r.status_code == HTTPStatus.UNAUTHORIZED):
        pass
    else:
        print(r.status_code, r.text)

    r = requests.put(f"{CATALOG}/actors", params={"name": "Chris Hemsworth", "birthdate": "1977-09-15"},
                     headers=headers_admin)
    if ok("Añadir actor por usuario admin", r.status_code == HTTPStatus.CREATED and r.json()):
        pass
    else:
        print(r.status_code, r.text)

    r = requests.put(f"{CATALOG}/actors", params={"name": "Chris Hemsworth", "birthdate": "1977-09-15"},
                    headers=headers_admin)
    if ok("Intento de añadir actor ya existente", r.status_code == HTTPStatus.CONFLICT):
        pass
    else:
        print(r.status_code, r.text)

    r = requests.get(f"{CATALOG}/actors", params={"name": "Chris Hemsworth", "birthdate": "1984-11-22"},
                    headers=headers_admin)
    if ok("Buscar actor 'Chris Hemsworth'", r.status_code == HTTPStatus.OK and r.json()):
        actor_id = r.json()[0]['actorid']
    else:
        print(r.status_code, r.text)

    r = requests.delete(f"{CATALOG}/actors/{actor_id}", headers=headers_admin)
    if ok("Eliminar actor por usuario admin", r.status_code == HTTPStatus.OK):
        pass
    else:
        print(r.status_code, r.text)

    r = requests.delete(f"{CATALOG}/actors/99999999", headers=headers_admin)
    if ok("Intento de eliminar actor inexistente", r.status_code == HTTPStatus.NOT_FOUND):
        pass
    else:
        print(r.status_code, r.text)

    r = requests.delete(f"{CATALOG}/actors/hola", headers=headers_admin)
    if ok("Intento de eliminar actor con ID no numérico", r.status_code == HTTPStatus.BAD_REQUEST):
        pass
    else:
        print(r.status_code, r.text)

    r = requests.get(f"{CATALOG}/movies", params={"year" : 2001}, headers=headers_alice)
    movieid = r.json()[0]['movieid']
    r = requests.put(f"{CATALOG}/movies/{movieid}",params = {"actor_id": 999999, "character": "Saruman"}, headers=headers_admin)
    if ok("Asignar actor que no existe a una pelicula", r.status_code == HTTPStatus.NOT_FOUND):
        pass
    else:
        print(r.status_code, r.text)
    r = requests.put(f"{CATALOG}/actors", params={"name": "Christopher Lee", "birthdate": "1922-05-27"},headers=headers_admin)
    if ok("Añadir actor Christopher Lee por usuario admin", r.status_code == HTTPStatus.CREATED and r.json(),silent = True):
        actor_id = r.json()['actorid']
    else:
        print(r.status_code, r.text)

    r = requests.put(f"{CATALOG}/movies/abc",params = {"actor_id": 2, "character": "Saruman"}, headers=headers_admin)
    if ok("Asignar un actor a una película con id no numérico", r.status_code == HTTPStatus.BAD_REQUEST):
        pass
    else:
        print(r.status_code, r.text)

    r = requests.put(f"{CATALOG}/movies/{movieid}",params = {"actor_id": "hola", "character": "Saruman"}, headers=headers_admin)
    if ok("Asignar actor con id no numérico a una pelicula", r.status_code == HTTPStatus.BAD_REQUEST):
        pass
    else:
        print(r.status_code, r.text)

    r = requests.put(f"{CATALOG}/movies/{movieid}",params = {"actor_id": actor_id, "character": "Saruman"}, headers=headers_admin)
    if ok("Asignar actor existente a una pelicula", r.status_code == HTTPStatus.OK):
        pass
    else:
        print(r.status_code, r.text)
    
    r = requests.put(f"{CATALOG}/movies/{movieid}",params = {"actor_id": actor_id, "character": "Saruman"}, headers=headers_admin)
    if ok("Asignar mismo actor nuevamente a una pelicula", r.status_code == HTTPStatus.CONFLICT):
        pass
    else:
        print(r.status_code, r.text)

    r = requests.put(f"{CATALOG}/movies/{movieid}",headers=headers_alice)
    if ok("Intento de añadir un actor a una película por un usuario no admin", r.status_code == HTTPStatus.UNAUTHORIZED):
        pass
    else:
        print(r.status_code, r.text)


    r = requests.put(f"{CATALOG}/movies/999999",params = {"actor_id": actor_id, "character": "Saruman"}, headers=headers_admin)
    if ok("Asignar actor a una pelicula que no existe", r.status_code == HTTPStatus.NOT_FOUND):
        pass
    else:
        print(r.status_code, r.text)

    r = requests.delete(f"{CATALOG}/movies/{movieid}/{actor_id}",params = {"character": "Saruman"}, headers=headers_admin)
    if ok("Eliminar actor de una película", r.status_code == HTTPStatus.OK):
        pass
    else:
        print(r.status_code, r.text)

    return movieids

def teardown(headers_admin):
    r = requests.get(f"{CATALOG}/actors", params={"name": "Christopher Lee"},headers=headers_admin)
    actor_id = r.json()[0]['actorid']
    r = requests.delete(f"{CATALOG}/actors/{actor_id}", headers=headers_admin)

if __name__ == "__main__":
    # Recuperar el usuario alice para obtener su token
    headers_alice, uid_alice, headers_admin, uid_admin = cliente_users.setup(silent = True)
    main(headers_alice, headers_admin)
    teardown(headers_admin)
    cliente_users.teardown(headers_admin, uid_alice, silent = True)

    from urls import test_passed, test_failed
    
    print(f"\nPruebas completadas. Test pasados: {test_passed} / {test_passed + test_failed}")