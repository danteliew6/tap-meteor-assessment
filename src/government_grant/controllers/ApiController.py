from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from ..models.FamilyMember import FamilyMember
from ..models.Household import Household
from flask_cors import CORS
from sqlalchemy import not_, func
from src.government_grant import db
from datetime import datetime
import json
import functools
from jsonschema import validate


class ApiController():
    def createHousehold():
        schema = {
            "type" : "object",
            "properties" : {
                "household_type" : {
                    "type" : "string",
                    "enum": ["HDB", "Condominium", "Landed"]
                    }
            },
            "required": ["household_type"]
        }
        try:
            data = request.get_json()
            validate(data, schema=schema)
            household = Household(household_type = data['household_type'])
            db.session.add(household)
            db.session.commit()
            return jsonify({
                "data": {
                    "household": household.to_dict()
                }
            }), 201
        except Exception as e:
            return jsonify({
                "message": str(e)
            }), 400
    
    def addFamilyMember():
        schema = {
            "type" : "object",
            "properties" : {
                "name": {
                    "type": "string"
                    },
                "gender": {
                    "type": "string"
                    },
                "marital_status" : {
                    "type": "string"
                    },
                "spouse" : {
                    "type": ["string", 'null']
                    },
                "occupation_type" : {
                    "type": "string",
                    "enum": ["Unemployed", "Student", "Employed"]
                    },
                "annual_income" : {
                    "type" : ["integer", "string"]
                    },
                "dob" : {
                    "type" : "string",
                    "format": "date-time"
                    },
                "household_id": {
                    "type": "integer"
                    }
            },
            "required": ["household_id", "name", "dob", "annual_income", "occupation_type", "marital_status", "gender", "spouse"]
        }
        try:
            data = request.get_json()
            validate(data, schema=schema)
            dob = datetime.strptime(data['dob'], '%d/%m/%Y').date()
            family_member = FamilyMember(
                name = data['name'],
                gender = data['gender'].lower(),
                marital_status  = data['marital_status'].lower(),
                spouse = data['spouse'],
                occupation_type  = data['occupation_type'].lower(),
                annual_income  = data['annual_income'],
                dob  = dob,
                household_id  = data['household_id']
            )
            db.session.add(family_member)
            db.session.commit()
            return jsonify({
                "data": {
                    "family_member": family_member.to_dict()
                }
            }), 201
        except Exception as e:
            return jsonify({
                "message": str(e)
            }), 400
    
    def getAllHouseholds():
        try:
            households = Household.query.all()
            households_and_families = []
            for household in households:
                household_details = household.to_dict()
                family = []
                for family_members in household.family_members:
                    family.append(family_members.to_dict())
                household_details['family_members'] = family
                households_and_families.append(household_details)
                
            return jsonify({
                "data": {
                    "households": households_and_families
                }
            }), 200
        except Exception as e:
            return jsonify({
                "message": str(e)
            }), 400
    
    def getHousehold():
        try:
            args = request.args
            household_id = args['household_id']
            household = Household.query.filter(Household.household_id == household_id).first()
            if household == None:
                raise Exception("Household not found")
            
            household_details = household.to_dict()
            family = []
            for family_members in household.family_members:
                    family.append(family_members.to_dict())
            household_details['family_members'] = family
            
            return jsonify({
                "data": {
                    "household": household_details
                }
            }), 200
        except Exception as e:
            return jsonify({
                "message": str(e)
            }), 400
    
    
    def listQualifiedHouseholds():
        households = Household.query.all()
        result = {
            "student_encouragement_bonus": [],
            "multigeneration_scheme": [],
            "elder_bonus": [],
            "baby_sunshine_grant ": [],
            "yolo_gst_grant": []
        }
        try:
            for household in households:
                household.getEligibleGrants(result)

            return jsonify({
                    "data": result
                }), 200
        except Exception as e:
            return jsonify({
                "message": str(e)
            }), 400