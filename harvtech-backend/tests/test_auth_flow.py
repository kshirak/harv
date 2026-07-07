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
        self.assertEqual(login_response.json()["message"], "Login successful")


if __name__ == "__main__":
    unittest.main()
