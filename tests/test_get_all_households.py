# Third party modules
import json
import unittest
# First party modules
from src.government_grant import app, db
from src.government_grant.models.Household import Household
from src.government_grant.models.FamilyMember import FamilyMember
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta   

class TestGetAllHouseholds(unittest.TestCase):
    def setUp(self):
        self.app =app
        app.config["TESTING"] = True
        app.testing=True
        app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root@localhost:3306/government_grant_test'
        app.app_context().push()
        db.create_all()
        db.session.rollback()
        household1 = Household(household_type="HDB")
        db.session.add(household1)
        household2 = Household(household_type="Landed")
        db.session.add(household2)
        db.session.flush()
        today = datetime.today()
        age = today - relativedelta(years = 25)
        member1 = FamilyMember(
                name = "member1",
                gender = "male",
                marital_status  = "single",
                spouse = None,
                occupation_type  = "employed",
                annual_income  = 99999,
                dob  = age,
                household_id  = household1.household_id
            )
        member2 = FamilyMember(
                name = "member2",
                gender = "male",
                marital_status  = "single",
                spouse = None,
                occupation_type  = "unemployed",
                annual_income  = 0,
                dob  = age,
                household_id  = household2.household_id
            )
        db.session.add(member1)
        db.session.add(member2)
        db.session.commit()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app = None

    def test_happy_path(self):
        response = self.client.get('/api/get-all-households', headers={"Content-Type":"application/json"})
        self.assertEqual(200, response.status_code)
        response_json = json.loads(response.data)
        # To return 2 household consisting of 1 family member each
        self.assertNotEqual({}, response_json['data']['households'])
        self.assertEqual(2, len(response_json['data']['households']))
        self.assertEqual(1, len(response_json['data']['households'][0]['family_members']))
        self.assertEqual(1, len(response_json['data']['households'][1]['family_members']))
