import pytest
from fastapi import HTTPException

from app.security import hash_password, verify_password, create_access_token, decode_token


class TestSecurity:
    # test hash generation and verification
    def test_hash_password(self):
        password = 'test_password'

        hashed_password = hash_password(password)

        assert verify_password(password, hashed_password)


    # test token generation and decoding
    def test_token(self):
        data = {"username": "test_user"}

        token = create_access_token(data)
        decoded_data = decode_token(token)

        assert decoded_data is not None
        assert decoded_data["username"] == "test_user"


    # test token generation with invalid input
    def test_invalid_token_generation(self):
        with pytest.raises((TypeError, AttributeError)):
            create_access_token('')


    # test invalid token decode
    def test_invalid_decode(self):
        token = "invalid"

        with pytest.raises(HTTPException):
            decode_token(token)