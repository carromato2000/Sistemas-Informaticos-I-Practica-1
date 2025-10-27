USERS = "http://127.0.0.1:5050"
CATALOG = "http://127.0.0.1:5051"

test_passed = 0 
test_failed = 0

def ok(name, cond, silent=False):
    status = "OK" if cond else "FAIL"
    if not silent: print(f"[{status}] {name}")
    if cond:
        status = "OK"
        global test_passed
        test_passed += 1
    else:
        status = "FAIL"
        global test_failed
        test_failed += 1
    return cond