import requests
from http import HTTPStatus
import cliente_users
import cliente_movies
import cliente_carts

from urls import USERS, CATALOG, ok


def ok(name, cond):
    status = "OK" if cond else "FAIL"
    print(f"[{status}] {name}")
    return cond

def main():
    headers_alice, uid_alice, headers_admin = cliente_users.main()

    movieids = cliente_movies.main(headers_alice)

    cliente_carts.main(headers_alice, movieids)

    
    print("# =======================================================")
    print("# Limpiar base de datos")
    print("# =======================================================")

    cliente_users.teardown(headers_admin, uid_alice)
    
    print("\nPruebas completadas.")

if __name__ == "__main__":
    main()
