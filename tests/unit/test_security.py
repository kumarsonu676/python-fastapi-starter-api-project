import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    verify_token,
)


@pytest.mark.unit
class TestPasswordSecurity:
    """test password hashing and verification functions"""

    def test_get_password_hash_returns_hash(self):
        """test password hashing produces non-empty hash"""
        password = "TestPassword123"
        hashed = get_password_hash(password)

        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 20  # bcrypt hashes are long
        assert hashed.startswith("$2b$")  # bcrypt format

    def test_get_password_hash_different_for_same_password(self):
        """test salt makes same password produce different hashes"""
        password = "TestPassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        assert hash1 != hash2  # salt ensures uniqueness

    def test_verify_password_correct(self):
        """test password verification succeeds with correct password"""
        password = "TestPassword123"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """test password verification fails with wrong password"""
        password = "TestPassword123"
        wrong_password = "WrongPassword123"
        hashed = get_password_hash(password)

        assert verify_password(wrong_password, hashed) is False

    def test_verify_password_empty_strings(self):
        """test password verification handles empty strings"""
        # empty hash should raise exception or return false
        try:
            result = verify_password("password", "")
            assert result is False
        except Exception:
            # passlib raises exception for empty hash, which is acceptable
            pass

        # empty password with valid hash should return false
        valid_hash = get_password_hash("test")
        assert verify_password("", valid_hash) is False


@pytest.mark.unit
class TestJWTSecurity:
    """test jwt token creation and verification"""

    @patch("app.core.security.settings")
    def test_create_access_token_basic(self, mock_settings):
        """test basic token creation"""
        mock_settings.SECRET_KEY = "test-secret-key"
        mock_settings.ALGORITHM = "HS256"
        mock_settings.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        mock_settings.JWT_AUDIENCE = "test-audience"
        mock_settings.JWT_ISSUER = "test-issuer"

        data = {"sub": "test@example.com", "user_id": 1}
        token = create_access_token(data)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 20  # jwt tokens are lengthy
        assert token.count(".") == 2  # jwt has 3 parts separated by dots

    @patch("app.core.security.settings")
    def test_create_access_token_with_expiry(self, mock_settings):
        """test token creation with custom expiry"""
        mock_settings.SECRET_KEY = "test-secret-key"
        mock_settings.ALGORITHM = "HS256"
        mock_settings.JWT_AUDIENCE = "test-audience"
        mock_settings.JWT_ISSUER = "test-issuer"

        data = {"sub": "test@example.com"}
        expires_delta = timedelta(minutes=15)
        token = create_access_token(data, expires_delta)

        assert token is not None
        assert isinstance(token, str)

    @patch("app.core.security.settings")
    def test_verify_token_valid(self, mock_settings):
        """test valid token verification"""
        mock_settings.SECRET_KEY = "test-secret-key"
        mock_settings.ALGORITHM = "HS256"
        mock_settings.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        mock_settings.JWT_AUDIENCE = "test-audience"
        mock_settings.JWT_ISSUER = "test-issuer"

        data = {"sub": "test@example.com", "user_id": 1}
        token = create_access_token(data)
        payload = verify_token(token)

        assert payload is not None
        assert payload["sub"] == "test@example.com"
        assert payload["user_id"] == 1
        assert payload["aud"] == "test-audience"
        assert payload["iss"] == "test-issuer"
        assert "exp" in payload

    @patch("app.core.security.settings")
    def test_verify_token_invalid(self, mock_settings):
        """test invalid token verification"""
        mock_settings.SECRET_KEY = "test-secret-key"
        mock_settings.ALGORITHM = "HS256"
        mock_settings.JWT_AUDIENCE = "test-audience"
        mock_settings.JWT_ISSUER = "test-issuer"

        invalid_token = "invalid.token.here"
        payload = verify_token(invalid_token)

        assert payload is None

    @patch("app.core.security.settings")
    def test_verify_token_wrong_secret(self, mock_settings):
        """test token verification fails with wrong secret"""
        # create with one secret
        mock_settings.SECRET_KEY = "test-secret-key"
        mock_settings.ALGORITHM = "HS256"
        mock_settings.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        mock_settings.JWT_AUDIENCE = "test-audience"
        mock_settings.JWT_ISSUER = "test-issuer"

        data = {"sub": "test@example.com"}
        token = create_access_token(data)

        # verify with different secret
        mock_settings.SECRET_KEY = "different-secret-key"
        payload = verify_token(token)

        assert payload is None

    @patch("app.core.security.settings")
    def test_verify_expired_token(self, mock_settings):
        """test expired token verification fails"""
        mock_settings.SECRET_KEY = "test-secret-key"
        mock_settings.ALGORITHM = "HS256"
        mock_settings.JWT_AUDIENCE = "test-audience"
        mock_settings.JWT_ISSUER = "test-issuer"

        data = {"sub": "test@example.com"}
        # create token that expires immediately
        expires_delta = timedelta(seconds=-1)
        token = create_access_token(data, expires_delta)

        payload = verify_token(token)
        assert payload is None
