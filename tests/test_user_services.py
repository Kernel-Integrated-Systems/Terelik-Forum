import unittest

import pytest
from unittest.mock import patch
from modules.users import User
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


    def test_un_authenticate_user(self):
        with patch('services.user_services.un_authenticate_user') as mock_un_auth:
            mock_un_auth.return_value = {"message": "User alice successfully logged out."}
            result = service.logout_user('alice')
            expected = {"message": "User alice successfully logged out."}
            self.assertEqual(expected, result)

    @patch('services.user_services.read_query')
    def test_authenticate(self, mock_read_query):
        with patch('services.user_services.authenticate') as mock_auth:
            mock_read_query.return_value = [
                {
                    "user_id": 1,
                    "username": "alice",
                    "password_hash": "hashed_password_1",  # This matches the test input password
                    "user_role": 1
                }
            ]
            result = service.authenticate_user('alice', 'hashed_password_1')
            expected = True
            self.assertEqual(expected, result)


    def test_authorise_user_role(self):
        with patch('services.user_services.authorise_user_role') as mock_auth_role:
            mock_auth_role.return_value = 1
            result = service.authorise_user_role('alice', 1)
            expected = 1
            self.assertEqual(expected, result)
