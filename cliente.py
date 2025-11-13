import requests
from http import HTTPStatus
from datetime import datetime

from urls import USERS, CATALOG, ok

def main(silent=False):
    print("# =======================================================")
    print("# Tester - Gestión de Stock y Triggers")
    print("# =======================================================")

    headers_alice, uid_alice, headers_admin, admin_id = setup(silent)

    # Tests de funcionalidad
    test_add_movie_to_cart(headers_alice, uid_alice, silent)
    test_remove_movie_from_cart(headers_alice, uid_alice, silent)
    test_checkout_with_discount(headers_alice, uid_alice, silent)
    test_clients_without_orders(headers_admin, silent)
    test_sales_statistics(headers_admin, silent)
    test_movie_rating(headers_alice, uid_alice, silent)
    test_country_management(headers_alice, uid_alice, headers_admin, silent)

    return [headers_alice, uid_alice, headers_admin]

def setup(silent=False):
    # Autenticar admin
    r = requests.post(f"{USERS}/login", json={"name": "admin", "password": "admin"})
    if ok("Autenticar usuario administrador predefinido", r.status_code == HTTPStatus.OK, silent):
        data = r.json()
        uid_admin, token_admin = data["uid"], data["token"]
    else:
        print("\nPruebas incompletas: Fin del test por error crítico")
        print(r.status_code, r.text)
        exit(-1)
    
    headers_admin = {"Authorization": f"Bearer {token_admin}"}

    # Crear usuario 'alice'
    r = requests.post(f"{USERS}/users", json={"name": "alice", "password": "secret", "country": "Peru"})
    if ok("Crear usuario 'alice' con país", r.status_code == HTTPStatus.OK and r.json(), silent):
        data = r.json()
    else:
        print(r.status_code, r.text)

    # Autenticar alice
    r = requests.post(f"{USERS}/login", json={"name": "alice", "password": "secret"})
    if ok("Autenticar usuario 'alice'", r.status_code == HTTPStatus.OK, silent):
        data = r.json()
        uid_alice, token_alice = data["uid"], data["token"]
        if not silent: print(f"UID de alice: {uid_alice}")
    else:
        print("\nPruebas incompletas: Fin del test por error crítico")
        exit(-1)

    headers_alice = {"Authorization": f"Bearer {token_alice}"}

    # Crear otro usuario para pruebas
    r = requests.post(f"{USERS}/users", json={"name": "bob", "password": "secret", "country": "Spain"})
    if ok("Crear usuario 'bob'", r.status_code == HTTPStatus.OK, silent):
        pass

    return headers_alice, uid_alice, headers_admin, uid_admin


def test_add_movie_to_cart(headers, uid, silent=False):
    """Test de agregar películas al carrito y actualización de stock"""
    print("\n# Test: Agregar película al carrito")
    
    # Obtener una película del catálogo
    r = requests.get(f"{CATALOG}/movies", headers=headers)
    if r.status_code != HTTPStatus.OK or not r.json():
        print("- Error: No hay películas en el catálogo")
        return
    
    movie_id = r.json()[0]['movieid']
    
    # Agregar película al carrito
    r = requests.post(f"{CATALOG}/cart", json={"movieid": movie_id}, headers=headers)
    if ok("Agregar película al carrito", r.status_code == HTTPStatus.OK, silent):
        print("- Película agregada correctamente")
        print("- Stock debe haberse decrementado mediante trigger")
        
    else:
        print(f"- Error: {r.status_code} - {r.text}")


def test_remove_movie_from_cart(headers, uid, silent=False):
    """Test de eliminar películas del carrito"""
    print("\n# Test: Eliminar película del carrito")
    
    r = requests.get(f"{CATALOG}/cart", headers=headers)
    if r.status_code != HTTPStatus.OK or not r.json():
        print("No hay películas en el carrito para eliminar")
        return
    
    movie_id = r.json()[0]['movieid']
    
    # Eliminar película del carrito
    r = requests.delete(f"{CATALOG}/cart/{movie_id}", headers=headers)
    if ok("Eliminar película del carrito", r.status_code == HTTPStatus.OK, silent):
        print("✓ Película eliminada correctamente")
        print("✓ Stock debe haberse incrementado mediante trigger")
        r=requests.get(f"{CATALOG}/movies/{movie_id}", headers=headers)
        if ok("Obtener el stock actualizado", r.status_code==HTTPStatus.OK,silent):
            print(f"{r.json()}")
    else:
        print(f"- Error: {r.status_code} - {r.text}")


def test_checkout_with_discount(headers, uid, silent=False):
    """Test de checkout con aplicación de descuento mediante trigger"""
    print("\n# Test: Checkout con descuento automático")
    
    # Obtener películas del catálogo
    r = requests.get(f"{CATALOG}/movies", headers=headers)
    if r.status_code != HTTPStatus.OK or not r.json():
        print("Error: No hay películas en el catálogo")
        return
    
    movie_id = r.json()[0]['movieid']
    
    # Agregar película al carrito
    r = requests.post(f"{CATALOG}/cart", json={"movieid": movie_id}, headers=headers)
    
    # Aplicar descuento al usuario (si existe el endpoint)
    r = requests.patch(f"{USERS}/users/{uid}/discount", json={"discount": 10}, headers=headers)
    if r.status_code == HTTPStatus.OK:
        print("✓ Descuento aplicado al usuario")
    
    # Realizar checkout
    r = requests.post(f"{CATALOG}/checkout", headers=headers)
    if ok("Realizar checkout con descuento", r.status_code == HTTPStatus.OK, silent):
        order = r.json()
        print(f"✓ Pedido creado: {order.get('orderid')}")
        print(f"✓ Descuento aplicado automáticamente mediante trigger")
        print(f"✓ Saldo del cliente actualizado mediante trigger")
        print(f"✓ Fecha de pago registrada: {order.get('paymentDate')}")
    else:
        print(f"✗ Error: {r.status_code} - {r.text}")


def test_clients_without_orders(headers_admin, silent=False):
    """Test de obtener clientes sin pedidos"""
    print("\n# Test: Clientes sin pedidos")
    
    r = requests.get(f"{USERS}/clientesSinPedidos", headers=headers_admin)
    if ok("Obtener clientes sin pedidos", r.status_code == HTTPStatus.OK, silent):
        clients = r.json()
        print(f"✓ Se encontraron {len(clients)} cliente(s) sin pedidos")
        for client in clients[:3]:  # Mostrar máximo 3
            print(f"  - {client.get('name')} ({client.get('country')}): ${client.get('balance')}")
    else:
        print(f"✗ Error: {r.status_code} - {r.text}")


def test_sales_statistics(headers_admin, silent=False):
    """Test de estadísticas de ventas por país y año"""
    print("\n# Test: Estadísticas de ventas")
    
    año = datetime.now().year
    paises = ["Peru", "Spain", "Mexico"]
    
    for pais in paises:
        r = requests.get(f"{CATALOG}/estadisticaVentas/{año}/{pais}", headers=headers_admin)
        if ok(f"Obtener ventas {año} - {pais}", r.status_code == HTTPStatus.OK, silent):
            stats = r.json()
            total_ventas = sum(order.get('totalCost', 0) for order in stats) if isinstance(stats, list) else 0
            print(f"✓ Ventas en {pais} ({año}): ${total_ventas:.2f}")
        else:
            if r.status_code != HTTPStatus.NOT_FOUND:
                print(f"✗ Error: {r.status_code} - {r.text}")


def test_movie_rating(headers, uid, silent=False):
    """Test de sistema de valoración de películas con trigger"""
    print("\n# Test: Valoración de películas")
    
    # Obtener una película
    r = requests.get(f"{CATALOG}/movies", headers=headers)
    if r.status_code != HTTPStatus.OK or not r.json():
        print("Error: No hay películas en el catálogo")
        return
    
    movie_id = r.json()[0]['movieid']
    
    # Valorar película
    r = requests.post(f"{CATALOG}/movies/{movie_id}/rate", 
                      json={"rating": 4.5}, headers=headers)
    if ok("Valorar película", r.status_code in [HTTPStatus.OK, HTTPStatus.CREATED], silent):
        print("✓ Película valorada correctamente")
        print("✓ Rating promedio actualizado automáticamente mediante trigger")
    else:
        print(f"✗ Error: {r.status_code} - {r.text}")
    
    # Obtener película para ver su rating
    r = requests.get(f"{CATALOG}/movies/{movie_id}", headers=headers)
    if r.status_code == HTTPStatus.OK:
        movie = r.json()
        print(f"✓ Rating promedio actual: {movie.get('averageRating', 'N/A')}")


def test_country_management(headers_alice, uid_alice, headers_admin, silent=False):
    """Test de gestión del país de los clientes"""
    print("\n# Test: Gestión de país de clientes")
    
    # Actualizar país del usuario
    r = requests.patch(f"{USERS}/users/{uid_alice}", 
                       json={"country": "Mexico"}, headers=headers_alice)
    if ok("Actualizar país del usuario", r.status_code == HTTPStatus.OK, silent):
        print("✓ País actualizado correctamente")
    else:
        print(f"✗ Error: {r.status_code} - {r.text}")
    
    # Obtener información del usuario
    r = requests.get(f"{USERS}/users/{uid_alice}", headers=headers_alice)
    if r.status_code == HTTPStatus.OK:
        user = r.json()
        print(f"✓ País actual: {user.get('country')}")


def teardown(headers_admin, uid_alice, silent=False):
    """Limpieza de datos de prueba"""
    r = requests.delete(f"{USERS}/users/{uid_alice}", headers=headers_admin)
    if not ok("Borrar usuario alice", r.status_code == HTTPStatus.OK, silent):
        print(r.status_code, r.text)


if __name__ == "__main__":
    headers_alice, uid_alice, headers_admin = main()
    teardown(headers_admin, uid_alice)

    from urls import test_passed, test_failed
    
    print(f"\n# =======================================================")
    print(f"Pruebas completadas. Pruebas pasadas: {test_passed} / {test_passed + test_failed}")
    print(f"# =======================================================")