import unittest

import pytest
from unittest.mock import patch
from models.users import User
from services import user_services as service

# Mock Data
mock_user = {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "role": 1,
    "is_active": True
}

def create_user():
    return User(
        id=mock_user["id"],
        username=mock_user["username"],
        email=mock_user["email"],
        role=mock_user["role"],
        is_active=mock_user["is_active"]
    )


class UserService_Should(unittest.TestCase):

    def test_get_all_users(self):
        with patch('services.user_services.get_all_users') as mock_get:
            mock_get.return_value = [mock_user]
            result = service.get_all_users()
            result_obj = [User(**user_dict) for user_dict in result]
            expected = [create_user()]
            self.assertEqual(expected, result_obj)


    def test_get_user_by_id(self):
        with patch('services.user_services.get_user_by_id') as mock_get:
            mock_get.return_value = mock_user
            result = service.get_user_by_id(1)
            result_obj = User(**result)
            expected = create_user()
            self.assertEqual(expected, result_obj)

    def test_get_user_by_nonexistent_id(self):
        with patch('services.user_services.get_user_by_id') as mock_get:
            mock_get.side_effect = ValueError("User with ID 999 does not exist.")
            with self.assertRaises(ValueError) as context:
                service.get_user_by_id(999)
            self.assertEqual(str(context.exception), "User with ID 999 does not exist.")


    def test_get_user_by_email(self):
        with patch('services.user_services.get_user_by_email') as mock_get:
            mock_get.return_value = mock_user
            result = service.get_user_by_email('testuser@test.com')
            result_obj = User(**result)
            expected = create_user()
            self.assertEqual(expected, result_obj)


    def test_get_user_by_username(self):
        with patch('services.user_services.get_user_by_username') as mock_get:
            mock_get.return_value = mock_user
            result = service.get_user_by_username('alice')
            result_obj = User(**result)
            expected = create_user()
            self.assertEqual(expected, result_obj)

    def test_register_user_with_duplicate_username(self):
        with patch('services.user_services.register_user') as mock_register:
            mock_register.side_effect = ValueError("Username alice is already taken!")
            with self.assertRaises(ValueError) as context:
                service.register_user('alice', 'newuser@test.com', 'password')
            self.assertEqual(str(context.exception), "Username alice is already taken!")


    def test_register_user_with_duplicate_email(self):
        with patch('services.user_services.register_user') as mock_register:
            mock_register.side_effect = ValueError("Email is alice@example.com already registered!")
            with self.assertRaises(ValueError) as context:
                service.register_user('newuser', 'alice@example.com', 'password')
            self.assertEqual(str(context.exception), "Email is alice@example.com already registered!")


    def test_authenticate_user_with_invalid_password(self):
        with patch('services.user_services.authenticate_user') as mock_auth:
            mock_auth.side_effect = ValueError("The provided password is incorrect! Please try again.")
            with self.assertRaises(ValueError) as context:
                service.authenticate_user('alice', 'wrong_password')
            self.assertEqual(str(context.exception), "The provided password is incorrect! Please try again.")


    def test_register_user(self):
        with patch('services.user_services.register_user') as mock_register:
            mock_register.return_value = mock_user
            result = service.register_user('testuser', 'testuser@test.com', 'password')
            result_obj = User(**result)
            expected = create_user()
            self.assertEqual(expected, result_obj)


    def test_authenticate_user(self):
        with patch('services.user_services.authenticate_user') as mock_auth:
            mock_auth.return_value = {"token": "mock_token", "token_type": "bearer"}
            result = service.authenticate_user('alice', 'hashed_password_1')
            expected = {"token": "mock_token", "token_type": "bearer"}
            self.assertEqual(expected, result)


    def test_logout_user_with_incorrect_token(self):
        with patch('services.user_services.logout_user') as mock_logout:
            mock_logout.side_effect = ValueError("User alice is not logged in.")
            with self.assertRaises(ValueError) as context:
                service.logout_user('alice', 'invalid_token')
            self.assertEqual(str(context.exception), "User alice is not logged in.")


    def test_logout_user(self):
        with patch('services.user_services.logout_user') as mock_logout:
            mock_logout.return_value = {"message": "User alice successfully logged out."}
            result = service.logout_user('alice', 'mock_token')
            expected = {"message": "User alice successfully logged out."}
            self.assertEqual(expected, result)

