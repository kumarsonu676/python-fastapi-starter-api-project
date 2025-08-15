import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreate, UserUpdate, UserLogin, UserResponse
from app.models.user import UserRole


@pytest.mark.unit
class TestUserCreateSchema:
    """ai generated test as example"""

    def test_valid_user_create(self):
        """test valid user creation data"""
        data = {
            "email": "test@example.com",
            "password": "ValidPassword123",
            "first_name": "Test",
            "last_name": "User",
            "role": UserRole.USER.value,
        }
        user = UserCreate(**data)

        assert user.email == "test@example.com"
        assert user.password == "ValidPassword123"
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.role == UserRole.USER.value

    def test_password_validation_no_digit(self):
        """test password validation fails without digit"""
        data = {
            "email": "test@example.com",
            "password": "NoDigitPassword",
            "first_name": "Test",
            "last_name": "User",
        }

        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**data)

        assert "Password must contain at least one digit" in str(exc_info.value)

    def test_password_validation_no_uppercase(self):
        """test password validation fails without uppercase"""
        data = {
            "email": "test@example.com",
            "password": "nouppercase123",
            "first_name": "Test",
            "last_name": "User",
        }

        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**data)

        assert "Password must contain at least one uppercase letter" in str(
            exc_info.value
        )

    def test_password_validation_no_lowercase(self):
        """test password validation fails without lowercase"""
        data = {
            "email": "test@example.com",
            "password": "NOLOWERCASE123",
            "first_name": "Test",
            "last_name": "User",
        }

        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**data)

        assert "Password must contain at least one lowercase letter" in str(
            exc_info.value
        )

    def test_password_validation_too_short(self):
        """test password validation fails if too short"""
        data = {
            "email": "test@example.com",
            "password": "Short1",
            "first_name": "Test",
            "last_name": "User",
        }

        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**data)

        assert "at least 8 characters" in str(exc_info.value)

    def test_invalid_email_format(self):
        """test email validation fails with invalid format"""
        data = {
            "email": "invalid-email",
            "password": "ValidPassword123",
            "first_name": "Test",
            "last_name": "User",
        }

        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**data)

        assert "value is not a valid email address" in str(exc_info.value)

    def test_name_too_long(self):
        """test name validation fails if too long"""
        long_name = "A" * 51  # too long
        data = {
            "email": "test@example.com",
            "password": "ValidPassword123",
            "first_name": long_name,
            "last_name": "User",
        }

        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**data)

        assert "at most 50 characters" in str(exc_info.value)


@pytest.mark.unit
class TestUserLoginSchema:
    """ai generated test as example"""

    def test_valid_login(self):
        """test valid login data"""
        data = {"email": "test@example.com", "password": "password123"}
        login = UserLogin(**data)

        assert login.email == "test@example.com"
        assert login.password == "password123"

    def test_empty_email(self):
        """test login validation fails with empty email"""
        data = {"email": "", "password": "password123"}

        with pytest.raises(ValidationError) as exc_info:
            UserLogin(**data)

        assert "Email is required" in str(exc_info.value)

    def test_empty_password(self):
        """test login validation fails with empty password"""
        data = {"email": "test@example.com", "password": ""}

        with pytest.raises(ValidationError) as exc_info:
            UserLogin(**data)

        assert "Password is required" in str(exc_info.value)

    def test_missing_email(self):
        """test login validation fails with missing email"""
        data = {"password": "password123"}

        with pytest.raises(ValidationError) as exc_info:
            UserLogin(**data)

        assert "field required" in str(exc_info.value)

    def test_missing_password(self):
        """test login validation fails with missing password"""
        data = {"email": "test@example.com"}

        with pytest.raises(ValidationError) as exc_info:
            UserLogin(**data)

        assert "field required" in str(exc_info.value)


@pytest.mark.unit
class TestUserUpdateSchema:
    """ai generated test as example"""

    def test_valid_update(self):
        """test valid update data"""
        data = {
            "email": "newemail@example.com",
            "first_name": "NewName",
            "last_name": "NewLast",
            "is_active": False,
        }
        update = UserUpdate(**data)

        assert update.email == "newemail@example.com"
        assert update.first_name == "NewName"
        assert update.last_name == "NewLast"
        assert update.is_active is False

    def test_partial_update(self):
        """test partial update with only some fields"""
        data = {"first_name": "OnlyFirst"}
        update = UserUpdate(**data)

        assert update.first_name == "OnlyFirst"
        assert update.email is None
        assert update.last_name is None
        assert update.is_active is None

    def test_empty_update(self):
        """test empty update is valid"""
        update = UserUpdate()

        assert update.email is None
        assert update.first_name is None
        assert update.last_name is None
        assert update.is_active is None

    def test_invalid_email_update(self):
        """test update validation fails with invalid email"""
        data = {"email": "invalid-email"}

        with pytest.raises(ValidationError) as exc_info:
            UserUpdate(**data)

        assert "value is not a valid email address" in str(exc_info.value)

    def test_name_length_validation(self):
        """test name length validation in update"""
        # too short
        data = {"first_name": "A"}
        with pytest.raises(ValidationError):
            UserUpdate(**data)

        # too long
        data = {"last_name": "A" * 51}
        with pytest.raises(ValidationError):
            UserUpdate(**data)
