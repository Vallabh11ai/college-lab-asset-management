from database import hash_password

def test_hash_is_deterministic():
    assert hash_password("abc") == hash_password("abc")

def test_hash_is_not_plaintext():
    assert hash_password("abc") != "abc"
