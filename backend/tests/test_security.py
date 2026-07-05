from app.utils.security import create_access_token, hash_password, verify_password, verify_token


def test_password_hash_round_trip():
    hashed = hash_password("StrongerPassword123")
    assert hashed != "StrongerPassword123"
    assert verify_password("StrongerPassword123", hashed)


def test_access_token_contains_subject():
    token = create_access_token({"sub": "user-id"})
    payload = verify_token(token)
    assert payload["sub"] == "user-id"
    assert payload["type"] == "access"
