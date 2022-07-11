# Third party modules
import json
import unittest
# First party modules
from src.government_grant import app, db
from src.government_grant.models.Household import Household
from src.government_grant.models.FamilyMember import FamilyMember
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta   

class TestStudentEncouragementBonus(unittest.TestCase):
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
        household1 = Household(household_type="Landed")
        db.session.add(household1)
        db.session.flush()
        today = datetime.today()
        eligible_age = today - relativedelta(years = 15)
        eligible_member = FamilyMember(
                name = "eligible member",
                gender = "male",
                marital_status  = "single",
                spouse = None,
                occupation_type  = "student",
                annual_income  = 199999,
                dob  = eligible_age,
                household_id  = household1.household_id
            )
        db.session.add(eligible_member)
        db.session.commit()
        response = self.client.get('/api/list-qualified-households', headers={"Content-Type":"application/json"})
        self.assertEqual(200, response.status_code)
        response_json = json.loads(response.data)
        # To return 1 household of 1 family member
        self.assertEqual(1, len(response_json['data']['student_encouragement_bonus']))
        self.assertEqual(1, len(response_json['data']['student_encouragement_bonus'][str(household1.household_id)]))
    
    def test_ineligible_age(self):
        household = Household(household_type="HDB")
        db.session.add(household)
        db.session.flush()
        today = datetime.today()
        ineligible_age = today - relativedelta(years = 16)
        ineligible_member = FamilyMember(
                name = "ineligible member",
                gender = "male",
                marital_status  = "single",
                spouse = None,
                occupation_type  = "student",
                annual_income  = 199999,
                dob  = ineligible_age,
                household_id  = household.household_id
            )
        db.session.add(ineligible_member)
        db.session.commit()
        response = self.client.get('/api/list-qualified-households', headers={"Content-Type":"application/json"})
        self.assertEqual(200, response.status_code)
        response_json = json.loads(response.data)
        # To return empty result
        self.assertEqual({}, response_json['data']['student_encouragement_bonus'])
        
    def test_ineligible_occupation(self):
        household = Household(household_type="HDB")
        db.session.add(household)
        db.session.flush()
        today = datetime.today()
        ineligible_age = today - relativedelta(years = 15)
        ineligible_member = FamilyMember(
                name = "ineligible member",
                gender = "male",
                marital_status  = "single",
                spouse = None,
                occupation_type  = "employed",
                annual_income  = 199999,
                dob  = ineligible_age,
                household_id  = household.household_id
            )
        db.session.add(ineligible_member)
        db.session.commit()
        response = self.client.get('/api/list-qualified-households', headers={"Content-Type":"application/json"})
        self.assertEqual(200, response.status_code)
        response_json = json.loads(response.data)
        # To return empty result
        self.assertEqual({}, response_json['data']['student_encouragement_bonus'])

    def test_ineligible_income(self):
        household = Household(household_type="HDB")
        db.session.add(household)
        db.session.flush()
        today = datetime.today()
        ineligible_age = today - relativedelta(years = 15)
        ineligible_member = FamilyMember(
                name = "ineligible member",
                gender = "male",
                marital_status  = "single",
                spouse = None,
                occupation_type  = "employed",
                annual_income  = 200000,
                dob  = ineligible_age,
                household_id  = household.household_id
            )
        db.session.add(ineligible_member)
        db.session.commit()
        response = self.client.get('/api/list-qualified-households', headers={"Content-Type":"application/json"})
        self.assertEqual(200, response.status_code)
        response_json = json.loads(response.data)
        # To return empty result
        self.assertEqual({}, response_json['data']['student_encouragement_bonus'])
