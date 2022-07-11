# Third party modules
import json
import unittest
# First party modules
from src.government_grant import app, db
from src.government_grant.models.Household import Household
from src.government_grant.models.FamilyMember import FamilyMember
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta   

class TestGetHousehold(unittest.TestCase):
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
        db.session.flush()
        today = datetime.today()
        age = today - relativedelta(years = 25)
        member = FamilyMember(
                name = "member",
                gender = "male",
                marital_status  = "single",
                spouse = None,
                occupation_type  = "employed",
                annual_income  = 99999,
                dob  = age,
                household_id  = household.household_id
            )
        same_household_member = FamilyMember(
                name = "same household member",
                gender = "male",
                marital_status  = "single",
                spouse = None,
                occupation_type  = "unemployed",
                annual_income  = 0,
                dob  = age,
                household_id  = household.household_id
            )
        db.session.add(member)
        db.session.add(same_household_member)
        db.session.commit()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app = None

    def test_happy_path(self):
        response = self.client.get('/api/get-household?household_id=1', headers={"Content-Type":"application/json"})
        self.assertEqual(200, response.status_code)
        response_json = json.loads(response.data)
        # To return 1 household of 2 family member
        self.assertNotEqual({}, response_json['data']['household'])
        self.assertEqual(2, len(response_json['data']['household']['family_members']))
    
    def test_non_existent_household(self):
        response = self.client.get('/api/get-household?household_id=2', headers={"Content-Type":"application/json"})
        # To return code 400
        self.assertEqual(400, response.status_code)