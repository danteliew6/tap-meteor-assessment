# Third party modules
import json
import unittest
# First party modules
from src.government_grant import app, db
from src.government_grant.models.Household import Household
from src.government_grant.models.FamilyMember import FamilyMember
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta   

class TestMultiGenerationScheme(unittest.TestCase):
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
        household = Household(household_type="Landed")
        db.session.add(household)
        db.session.flush()
        today = datetime.today()
        eligible_age = today - relativedelta(years = 17)
        eligible_member = FamilyMember(
                name = "eligible member",
                gender = "male",
                marital_status  = "single",
                spouse = None,
                occupation_type  = "student",
                annual_income  = 149999,
                dob  = eligible_age,
                household_id  = household.household_id
            )
        ineligible_age = today - relativedelta(years = 30)
        same_household_member = FamilyMember(
                name = "ineligible member but under same household of eligible member",
                gender = "male",
                marital_status  = "single",
                spouse = None,
                occupation_type  = "unemployed",
                annual_income  = 0,
                dob  = ineligible_age,
                household_id  = household.household_id
            )
        db.session.add(eligible_member)
        db.session.add(same_household_member)
        db.session.commit()
        response = self.client.get('/api/list-qualified-households', headers={"Content-Type":"application/json"})
        self.assertEqual(200, response.status_code)
        response_json = json.loads(response.data)
        # To return 1 household of 2 family members
        self.assertEqual(1, len(response_json['data']['multigeneration_scheme']))
        self.assertEqual(2, len(response_json['data']['multigeneration_scheme'][str(household.household_id)]))
    
    def test_ineligible_age(self):
        household = Household(household_type="Landed")
        db.session.add(household)
        db.session.flush()
        today = datetime.today()
        lower_ineligible_age = today - relativedelta(years = 18)
        ineligible_member = FamilyMember(
                name = "ineligible member 1",
                gender = "male",
                marital_status  = "single",
                spouse = None,
                occupation_type  = "student",
                annual_income  = 0,
                dob  = lower_ineligible_age,
                household_id  = household.household_id
            )
        upper_ineligible_age = today - relativedelta(years = 54)
        same_household_member = FamilyMember(
                name = "ineligible member 2",
                gender = "male",
                marital_status  = "single",
                spouse = None,
                occupation_type  = "unemployed",
                annual_income  = 0,
                dob  = upper_ineligible_age,
                household_id  = household.household_id
            )
        db.session.add(ineligible_member)
        db.session.add(same_household_member)
        db.session.commit()
        response = self.client.get('/api/list-qualified-households', headers={"Content-Type":"application/json"})
        self.assertEqual(200, response.status_code)
        response_json = json.loads(response.data)
        # To return empty result as age does not meet criteria
        self.assertEqual({}, response_json['data']['multigeneration_scheme'])
    
    def test_ineligible_income(self):
        household = Household(household_type="Landed")
        db.session.add(household)
        db.session.flush()
        today = datetime.today()
        lower_eligible_age = today - relativedelta(years = 17)
        eligible_member = FamilyMember(
                name = "eligible member 1",
                gender = "male",
                marital_status  = "single",
                spouse = None,
                occupation_type  = "employed",
                annual_income  = 75000,
                dob  = lower_eligible_age,
                household_id  = household.household_id
            )
        upper_eligible_age = today - relativedelta(years = 55)
        eligible_member_2 = FamilyMember(
                name = "eligible member 2",
                gender = "male",
                marital_status  = "single",
                spouse = None,
                occupation_type  = "employed",
                annual_income  = 75000,
                dob  = upper_eligible_age,
                household_id  = household.household_id
            )
        db.session.add(eligible_member)
        db.session.add(eligible_member_2)
        db.session.commit()
        response = self.client.get('/api/list-qualified-households', headers={"Content-Type":"application/json"})
        self.assertEqual(200, response.status_code)
        response_json = json.loads(response.data)
        # To return empty result as total income is 150k
        self.assertEqual({}, response_json['data']['multigeneration_scheme'])