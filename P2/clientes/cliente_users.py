import requests
from http import HTTPStatus

from urls import USERS, CATALOG, ok

def main(silent=False):
    print("# =======================================================")
    print("# Creación y autenticación de usuarios para el test")
    print("# =======================================================")

    headers_alice, uid_alice, headers_admin, admin_id = setup(silent)

    # Crear el usuario administrador de nuevo para probar la condición de conflicto
    r = requests.put(f"{USERS}/user", json={"name": "admin", "password": "admin"}, headers=headers_admin)
    if ok("Crear usuario administrador predefinido de nuevo", r.status_code == HTTPStatus.CONFLICT, silent):
        pass
    else:
        print(r.status_code, r.text)

    # Intentar borrar el usuario administrador predefinido
    r = requests.delete(f"{USERS}/user/{admin_id}", headers=headers_admin)
    if ok("Borrar usuario administrador predefinido", r.status_code == HTTPStatus.FORBIDDEN,silent):
        pass
    else:
        print(r.status_code, r.text)

    # Intentar autenticar un usuario inexistente
    r = requests.get(f"{USERS}/user", json={"name": "this user should not exist", "password": "nopassword"})
    if ok("Autenticar usuario inexistente", r.status_code == HTTPStatus.NOT_FOUND,silent):
        pass
    else:
        print(r.status_code, r.text)

    r = requests.put(f"{USERS}/user", json={"name": "luis", "password": "123"})
    if ok("Crear usuario 'luis' con contraseña débil", r.status_code == HTTPStatus.BAD_REQUEST,silent):
        pass
    else:
        print(r.status_code, r.text)

    r = requests.put(f"{USERS}/user", json={"password": "nopassword"})
    if ok("Crear usuario sin nombre", r.status_code == HTTPStatus.BAD_REQUEST,silent):
        pass
    else:
        print(r.status_code, r.text)

    r = requests.put(f"{USERS}/user", json={"name": "luis"})
    if ok("Crear usuario 'luis' sin contraseña", r.status_code == HTTPStatus.BAD_REQUEST,silent):
        pass   
    else:
        print(r.status_code, r.text) 

    r = requests.get(f"{USERS}/user", json={"name": "alice", "password": "wrongpassword"})
    if ok("Autenticar usuario 'alice' con contraseña incorrecta", r.status_code == HTTPStatus.UNAUTHORIZED,silent):
        pass
    else:
        print(r.status_code, r.text)

    # Intentar borrar un usuario inexistente
    r = requests.delete(f"{USERS}/user/1234", headers=headers_admin)
    if ok("Borrar usuario inexistente", r.status_code == HTTPStatus.NOT_FOUND,silent):
        pass
    else:
        print(r.status_code, r.text)

    return [headers_alice, uid_alice, headers_admin]

def setup(silent=False):
    r = requests.get(f"{USERS}/user", json={"name": "admin", "password": "admin"})
    if ok("Autenticar usuario administrador predefinido", r.status_code == HTTPStatus.OK,silent):
        data = r.json()
        uid_admin, token_admin = data["uid"], data["token"]
    else:
        print("\nPruebas incompletas: Fin del test por error crítico")
        print(r.status_code, r.text)
        exit(-1)
    
    headers_admin = {"Authorization": f"Bearer {token_admin}"}

        # Se asume que el usuario 'Alice' no existe
    r = requests.put(f"{USERS}/user", json={"name": "alice", "password": "secret"})
    if ok("Crear usuario 'alice'", r.status_code == HTTPStatus.OK and r.json(),silent):
        data = r.json()
    else:
        print(r.status_code, r.text)

    r = requests.get(f"{USERS}/user", json={"name": "alice", "password": "secret"})
    if ok("Autenticar usuario 'alice'", r.status_code == HTTPStatus.OK,silent):
        data = r.json()
        uid_alice, token_alice = data["uid"], data["token"]
        if not silent: print(f"UID de alice: {uid_alice}")
    else:
        print("\nPruebas incompletas: Fin del test por error crítico")

    headers_alice = {"Authorization": f"Bearer {token_alice}"}

    return headers_alice, uid_alice ,headers_admin,uid_admin


def teardown(headers_admin, uid_alice, silent=False):
    r = requests.delete(f"{USERS}/user/{uid_alice}", headers=headers_admin)
    ok("Borrar usuario alice", r.status_code == HTTPStatus.OK, silent)

if __name__ == "__main__":
    headers_alice, uid_alice, headers_admin = main()
    teardown(headers_admin, uid_alice)

    from urls import test_passed, test_failed
    
    print(f"\nPruebas completadas. Test pasados: {test_passed} / {test_passed + test_failed}")