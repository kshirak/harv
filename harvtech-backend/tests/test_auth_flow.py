import os
import sys
import unittest

from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./test_auth.db"

from app.core.database import Base, engine
from app.main import app


class AuthFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)

    def test_register_and_login_flow(self):
        register_payload = {
            "name": "Ravi Kumar",
            "place": "Coimbatore",
            "aadhar_number": "123456789012",
            "phone_number": "9876543210",
            "location": "Tamil Nadu",
            "acres_of_land": 5.5,
            "password": 1234,
        }

        response = self.client.post("/auth/register", json=register_payload)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["message"], "User registered successfully")
        self.assertEqual(body["fin_id"], "HT9876543210")

        login_response = self.client.post(
            "/auth/login",
            json={"fin_id": "HT9876543210", "password": 1234},
        )
        self.assertEqual(login_response.status_code, 200)
        login_body = login_response.json()
        self.assertTrue(login_body["success"])
        self.assertEqual(login_body["message"], "Login successful")
        self.assertIn("access_token", login_body)
        self.assertEqual(login_body["token_type"], "bearer")

    def test_get_user_details_by_fin_id(self):
        register_payload = {
            "name": "Ravi Kumar",
            "place": "Coimbatore",
            "aadhar_number": "123456789013",
            "phone_number": "9876543211",
            "location": "Tamil Nadu",
            "acres_of_land": 5.5,
            "password": 1234,
        }

        register_response = self.client.post("/auth/register", json=register_payload)
        self.assertEqual(register_response.status_code, 200)
        fin_id = register_response.json()["fin_id"]

        user_response = self.client.get(f"/auth/user/{fin_id}")
        self.assertEqual(user_response.status_code, 200)
        user_body = user_response.json()
        self.assertEqual(user_body["fin_id"], fin_id)
        self.assertEqual(user_body["name"], register_payload["name"])


if __name__ == "__main__":
    unittest.main()
