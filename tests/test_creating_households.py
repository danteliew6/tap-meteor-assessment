# Third party modules
import json
import unittest
# First party modules
from src.government_grant import app, db
from src.government_grant.models.Household import Household
from datetime import timedelta, datetime

class TestCreatingHouseholds(unittest.TestCase):
    def setUp(self):
        self.app =app
        app.config["TESTING"] = True
        app.testing=True
        app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root@localhost:3306/government_grant_test'
        app.app_context().push()
        db.create_all()
        db.session.rollback()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app = None

    def test_happy_path(self):
        data_json = {
            "household_type": "HDB"
        }
        response = self.client.post('/api/create-household', data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        self.assertEqual(201, response.status_code)
    
    def test_incorrect_datatype(self):
        data_json = {
            "household_type": 123
        }
        response = self.client.post('/api/create-household', data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        self.assertEqual(400, response.status_code)

    def test_incorrect_option(self):
        data_json = {
            "household_type": "House"
        }
        response = self.client.post('/api/create-household', data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        self.assertEqual(400, response.status_code)

