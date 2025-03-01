import unittest
import json
import os
import bcrypt
import jwt
import time
import socket
from enumeration import (
    load_users, save_users, hash_password, verify_password,
    generate_token, verify_token, SubdomainEnumerator, PortScanner
)

SECRET_KEY = "your_secret_key"

class TestAuthentication(unittest.TestCase):
    """Tests for user authentication functions"""

    def setUp(self):
        """Prepare a test user file"""
        self.test_users = {"testuser": hash_password("password123")}
        with open("test_users.json", "w") as f:
            json.dump(self.test_users, f)
    
    def tearDown(self):
        """Remove test user file"""
        if os.path.exists("test_users.json"):
            os.remove("test_users.json")

    def test_hash_password(self):
        """Ensure passwords are hashed correctly"""
        password = "securepassword"
        hashed = hash_password(password)
        self.assertTrue(verify_password(password, hashed))

    def test_verify_password(self):
        """Ensure correct password verification"""
        self.assertTrue(verify_password("password123", self.test_users["testuser"]))
        self.assertFalse(verify_password("wrongpass", self.test_users["testuser"]))

    def test_generate_token(self):
        """Ensure JWT token is generated correctly"""
        token = generate_token("testuser")
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        self.assertEqual(payload["user"], "testuser")

    def test_verify_token(self):
        """Ensure token verification works"""
        token = generate_token("testuser")
        self.assertEqual(verify_token(token), "testuser")

        # Test expired token
        expired_token = jwt.encode(
            {"user": "testuser", "exp": time.time() - 10},
            SECRET_KEY, algorithm="HS256"
        )
        self.assertIsNone(verify_token(expired_token))

class TestEnumeration(unittest.TestCase):
    """Tests for enumeration functionalities"""

    def test_subdomain_enumeration(self):
        """Ensure subdomain enumeration works"""
        enumerator = SubdomainEnumerator("example.com", ["www", "test", "dev"])
        result = enumerator.enumerate()
        self.assertIsInstance(result, list)

    def test_port_scanner(self):
        """Ensure port scanning works correctly"""
        enumerator = PortScanner("127.0.0.1", [22, 80, 443])
        result = enumerator.enumerate()
        self.assertIsInstance(result, list)

if __name__ == "__main__":
    unittest.main()



# import unittest
# from unittest.mock import patch, MagicMock
# from tkinter import Tk
# from enumeration_gui import WebEnumerationToolGUI
# from database import connect_db
# from enumeration_gui import register_user

# class TestWebEnumeration(unittest.TestCase):
    
#     @patch('database.connect_db')
#     def test_register_user(self, mock_connect_db):
#         """Test user registration with a mock database connection."""
#         mock_conn = MagicMock()
#         mock_cursor = MagicMock()
#         mock_conn.cursor.return_value = mock_cursor
#         mock_connect_db.return_value = mock_conn  # Ensure connect_db() returns mock connection

#         register_user("newuser", "password123")  # Call the function being tested

#         mock_cursor.execute.assert_called()  # Verify SQL execute() was called
#         mock_conn.commit.assert_called()     # Verify commit() was called

#     @patch('enumeration_gui.request_rate_limit')
#     def test_rate_limiting(self, mock_rate_limit):
#         """Test rate limiting in the GUI."""
#         root = Tk()  # Create a Tkinter root instance
#         gui = WebEnumerationToolGUI(root, "dummy_token")
        
#         mock_rate_limit.return_value = False  # Simulate no rate limit block
#         self.assertFalse(mock_rate_limit())

#     @patch('enumeration_gui.request_rate_limit')
#     def test_rate_limit_block(self, mock_rate_limit):
#         """Test if rate limiting correctly blocks excessive requests."""
#         root = Tk()  # Fix the NoneType issue
#         gui = WebEnumerationToolGUI(root, "dummy_token")
        
#         mock_rate_limit.return_value = True  # Simulate rate limit block
#         self.assertTrue(mock_rate_limit())

# if __name__ == "__main__":
#     unittest.main()

# # import unittest
# # import jwt
# # import bcrypt
# # import time
# # from unittest.mock import patch, MagicMock
# # from datetime import datetime, timedelta
# # from enumeration_gui import hash_password, verify_password, generate_token, verify_token, register_user, WebEnumerationToolGUI, LoginWindow
# # from database import connect_db

# # SECRET_KEY = "your_secret_key"

# # class TestWebEnumeration(unittest.TestCase):
    
# #     def test_hash_password(self):
# #         password = "securepassword"
# #         hashed = hash_password(password)
# #         self.assertTrue(isinstance(hashed, str))
# #         self.assertTrue(verify_password(password, hashed))

# #     def test_verify_password(self):
# #         password = "securepassword"
# #         hashed = hash_password(password)
# #         self.assertTrue(verify_password(password, hashed))
# #         self.assertFalse(verify_password("wrongpassword", hashed))

# #     def test_generate_token(self):
# #         token = generate_token("testuser")
# #         decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
# #         self.assertEqual(decoded["username"], "testuser")
# #         self.assertIn("exp", decoded)
    
# #     def test_verify_token(self):
# #         token = generate_token("testuser")
# #         self.assertEqual(verify_token(token), "testuser")
    
# #     def test_verify_expired_token(self):
# #         expired_token = jwt.encode({"username": "testuser", "exp": datetime.utcnow() - timedelta(seconds=1)}, SECRET_KEY, algorithm="HS256")
# #         self.assertIsNone(verify_token(expired_token))

# #     @patch("database.connect_db")
# #     def test_register_user(self, mock_db):
# #         mock_conn = MagicMock()
# #         mock_cursor = MagicMock()
# #         mock_db.return_value = mock_conn
# #         mock_conn.cursor.return_value = mock_cursor

# #         mock_cursor.fetchone.return_value = None  # Simulate new user
# #         register_user("newuser", "password123")
# #         mock_cursor.execute.assert_called()
# #         mock_conn.commit.assert_called()
    
# #     @patch("enumeration_gui.time.time", return_value=10000)
# #     def test_rate_limiting(self, mock_time):
# #         gui = WebEnumerationToolGUI(None, "dummy_token")
# #         gui.last_scan_time = 9990  # Last scan was 10 seconds ago
# #         self.assertIsNone(gui.run_enumeration())
    
# #     @patch("enumeration_gui.time.time", return_value=10005)
# #     def test_rate_limit_block(self, mock_time):
# #         gui = WebEnumerationToolGUI(None, "dummy_token")
# #         gui.last_scan_time = 10000  # Last scan just happened
# #         with patch("tkinter.messagebox.showerror") as mock_error:
# #             gui.run_enumeration()
# #             mock_error.assert_called_with("Error", "Rate Limit: Wait 10 seconds before scanning again!")

# #     @patch("enumeration_gui.messagebox.showinfo")
# #     def test_login_success(self, mock_messagebox):
# #         with patch("enumeration_gui.load_users", return_value={"testuser": hash_password("password")}):
# #             root = MagicMock()
# #             login_window = LoginWindow(root, lambda token: None)
# #             login_window.username_entry.get = MagicMock(return_value="testuser")
# #             login_window.password_entry.get = MagicMock(return_value="password")
# #             login_window.login()
# #             mock_messagebox.assert_called_with("Success", "Login Successful!")

# #     @patch("enumeration_gui.messagebox.showerror")
# #     def test_login_failure(self, mock_messagebox):
# #         with patch("enumeration_gui.load_users", return_value={"testuser": hash_password("password")}):
# #             root = MagicMock()
# #             login_window = LoginWindow(root, lambda token: None)
# #             login_window.username_entry.get = MagicMock(return_value="testuser")
# #             login_window.password_entry.get = MagicMock(return_value="wrongpassword")
# #             login_window.login()
# #             mock_messagebox.assert_called_with("Error", "Invalid Credentials")

# # if __name__ == "__main__":
# #     unittest.main()
