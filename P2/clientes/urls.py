USERS = "http://127.0.0.1:5050"
CATALOG = "http://127.0.0.1:5051"

def ok(name, cond, silent=False):
    status = "OK" if cond else "FAIL"
    if not silent: print(f"[{status}] {name}")
    return cond