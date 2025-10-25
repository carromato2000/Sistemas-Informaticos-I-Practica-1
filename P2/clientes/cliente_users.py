import requests
from http import HTTPStatus

from urls import USERS, CATALOG, ok


def main():
    print("# =======================================================")
    print("# Creación y autenticación de usuarios para el test")
    print("# =======================================================")

    # Usuario administrador por defecto, debe existir
    r = requests.get(f"{USERS}/user", json={"name": "admin", "password": "admin"})
    if ok("Autenticar usuario administrador predefinido", r.status_code == HTTPStatus.OK):
        data = r.json()
        _, token_admin = data["uid"], data["token"]
    else:
        print("\nPruebas incompletas: Fin del test por error crítico")
        print(r.status_code, r.text)
        exit(-1)
    
    headers_admin = {"Authorization": f"Bearer {token_admin}"}

    # Se asume que el usuario 'Alice' no existe
    r = requests.put(f"{USERS}/user", json={"name": "alice", "password": "secret"}, headers=headers_admin)
    if ok("Crear usuario 'alice'", r.status_code == HTTPStatus.OK and r.json()):
        data = r.json()
        uid_alice, _ = data["uid"], data["username"]
        
    else:
        print(r.status_code, r.text)
    

    r = requests.get(f"{USERS}/user", json={"name": "alice", "password": "secret"})
    if ok("Autenticar usuario 'alice'", r.status_code == HTTPStatus.OK):
        data = r.json()
        uid_alice, token_alice = data["uid"], data["token"]
        print(f"UID de alice: {uid_alice}")
    else:
        print("\nPruebas incompletas: Fin del test por error crítico")

    headers_alice = {"Authorization": f"Bearer {token_alice}"}

    return [headers_alice, uid_alice, headers_admin]

if __name__ == "__main__":
    main()