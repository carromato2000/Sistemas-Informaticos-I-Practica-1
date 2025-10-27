from http import HTTPStatus
import requests
from urls import CATALOG, ok

test_failed = 0
test_passed = 0

def main(headers_alice, movieids):
    print("# =======================================================")
    print("# Gestión del carrito de alice")
    print("# =======================================================")
    for movieid in movieids:
        r = requests.put(f"{CATALOG}/cart/{movieid}", headers=headers_alice)
        if ok(f"Añadir película con ID [{movieid}] al carrito", r.status_code == HTTPStatus.OK):
            r = requests.get(f"{CATALOG}/cart", headers=headers_alice)
            if ok("Obtener carrito del usuario con el nuevo contenido", r.status_code == HTTPStatus.OK and r.json()):
                data = r.json()
                if data:
                    for movie in data:
                        print(f"\t[{movie['movieid']}] {movie['title']} - {movie['price']}")
            
    if movieids:
        r = requests.put(f"{CATALOG}/cart/{movieids[0]}", headers=headers_alice)
        ok(f"Añadir película con ID [{movieids[0]}] al carrito más de una vez", r.status_code == HTTPStatus.CONFLICT)

        r = requests.delete(f"{CATALOG}/cart/{movieids[-1]}", headers=headers_alice)
        if ok(f"Elimimar película con ID [{movieids[-1]}] del carrito", r.status_code == HTTPStatus.OK):
            r = requests.get(f"{CATALOG}/cart", headers=headers_alice)
            if ok(f"Obtener carrito del usuario sin la película [{movieids[-1]}]", r.status_code == HTTPStatus.OK):
                data = r.json()
                if data:
                    for movie in data:
                        print(f"\t[{movie['movieid']}] {movie['title']} - {movie['price']}")
                else:
                    print("\tEl carrito está vacío.")
    
    r=requests.post(f"{CATALOG}/user/credit/{0}", headers=headers_alice)
    ok("Setear saldo a 0 para pruebas de checkout con saldo insuficiente", r.status_code == HTTPStatus.OK)
    
    r = requests.post(f"{CATALOG}/cart/checkout", headers=headers_alice)
    ok("Checkout del carrito con saldo insuficiente", r.status_code == HTTPStatus.PAYMENT_REQUIRED)

    r = requests.post(f"{CATALOG}/user/credit", json={"amount": 1200.75}, headers=headers_alice)
    if ok("Aumentar el saldo de alice", r.status_code == HTTPStatus.OK and r.json()):
        saldo = float(r.json()["new_credit"])
        print(f"\tSaldo actualizado a {saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    r = requests.post(f"{CATALOG}/user/credit", json={"amount": 1000000}, headers=headers_alice)
    if ok("Aumentar el saldo de alice", r.status_code == HTTPStatus.OK and r.json()):
        saldo = float(r.json()["new_credit"])
        print(f"\tSaldo actualizado a {saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    r = requests.post(f"{CATALOG}/cart/checkout", headers=headers_alice)
    if ok("Checkout del carrito", r.status_code == HTTPStatus.OK and r.json()):
        data = r.json()
        print(f"\tPedido {data['orderid']} creado correctamente:")

        r = requests.get(f"{CATALOG}/orders/{data['orderid']}", headers=headers_alice)
        if ok(f"Recuperar datos del pedido {data['orderid']}", r.status_code == HTTPStatus.OK and r.json()):
            order = r.json()
            print(f"\tFecha: {order['date']}\n\tPrecio: {order['total']}")
            print("\tContenidos:")
            for movie in order['movies']:
                    print(f"\t- [{movie['movieid']}] {movie['title']} ({movie['price']})")
        
        r = requests.get(f"{CATALOG}/cart", headers=headers_alice)
        ok("Obtener carrito vacío después de la venta", r.status_code == HTTPStatus.OK and not r.json())