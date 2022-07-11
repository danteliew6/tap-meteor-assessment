# Third party modules
import json
import unittest
# First party modules
from src.government_grant import app, db
from src.government_grant.models.Household import Household
from src.government_grant.models.FamilyMember import FamilyMember
from datetime import timedelta, datetime

class TestAddingFamilyMembers(unittest.TestCase):
    def setUp(self):
        self.app =app
        app.config["TESTING"] = True
        app.testing=True
        app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root@localhost:3306/government_grant_test'
        app.app_context().push()
        db.create_all()
        db.session.rollback()
        household = Household(household_type="HDB")
        db.session.add(household)
        db.session.commit()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app = None

    def test_happy_path(self):
        data_json = {
            "name" : "dante",
            "gender" : "male",
            "marital_status" : "single",
            "spouse": None,
            "occupation_type" : "Student",
            "annual_income" : 0,
            "dob" : "09/07/1997",
            "household_id": 1
        }
        response = self.client.post('/api/add-family-member', data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        self.assertEqual(201, response.status_code)
    
    def test_incorrect_data(self):
        data_json = {
            "name" : "dante",
            "gender" : "male",
            "marital_status" : "single",
            "spouse": None,
            "occupation_type" : "Student",
            "annual_income" : "0",
            "dob" : "09/07-1997",
            "household_id": 1
        }
        response = self.client.post('/api/add-family-member', data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        self.assertEqual(400, response.status_code)

    def test_incorrect_dob(self):
        data_json = {
            "name" : "dante",
            "gender" : "male",
            "marital_status" : "single",
            "spouse": None,
            "occupation_type" : "Student",
            "annual_income" : 0,
            "dob" : "09-07-1997",
            "household_id": 1
        }
        response = self.client.post('/api/add-family-member', data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        self.assertEqual(400, response.status_code)
    
    def test_incorrect_household_id(self):
        data_json = {
            "name" : "dante",
            "gender" : "male",
            "marital_status" : "single",
            "spouse": None,
            "occupation_type" : "Student",
            "annual_income" : 0,
            "dob" : "09-07-1997",
            "household_id": 10
        }
        response = self.client.post('/api/add-family-member', data=json.dumps(data_json), headers={"Content-Type":"application/json"})
        self.assertEqual(400, response.status_code)

