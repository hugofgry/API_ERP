import unittest
from fastapi.testclient import TestClient
from pydantic import BaseModel
from api import app
import os

client = TestClient(app)
token = os.environ.get("TOKENTEST_API_CRM")
if not isinstance(token, str):
        token = str(token)

class TestAPI(unittest.TestCase):

    def test_read_root(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Hello": "World"})

    

if __name__ == '__main__':
    unittest.main()