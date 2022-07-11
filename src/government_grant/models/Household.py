from src.government_grant import db
from .FamilyMember import FamilyMember
 


class Household(db.Model):
    # Start of DB model
    __tablename__ = 'households'
    __mapper_args__ = {'polymorphic_identity': 'households'}
    __table_args__={'mysql_engine':'InnoDB','mysql_auto_increment': '1'}

    household_id = db.Column(db.Integer(), primary_key = True, autoincrement=True)
    household_type = db.Column(db.String(50))
    family_members = db.relationship('FamilyMember')

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def evaluateStudentEncouragementBonus(self):
        income = 0
        eligible_members = []
        for family_member in self.family_members:
            income += family_member.annual_income
            if family_member.occupation_type == "student" and family_member.getAge() < 16:
                eligible_members.append(family_member)
        
        return [members.to_dict() for members in eligible_members] if income < 200000 and eligible_members != [] else None
        
    def evaluateMultiGenerationScheme(self):
        age_criteria = False
        income = 0
        for family_member in self.family_members:
            income += family_member.annual_income
            age = family_member.getAge()
            if age < 18 or age > 55:
                age_criteria = True
        
        return [family_member.to_dict() for family_member in self.family_members] if income < 150000 and age_criteria else None
    
    def evaluateElderBonus(self):
        if self.household_type != "HDB":
            return None
        eligible_members = []
        for family_member in self.family_members:
            if family_member.getAge() >= 55:
                eligible_members.append(family_member)
        
        return [eligible_member.to_dict() for eligible_member in eligible_members] if len(eligible_members) != 0 and eligible_members != [] else None
        
    def evaluateBabySunshineGrant(self):
        eligible_members = []
        for family_member in self.family_members:
            if family_member.getAgeByMonth() < 8:
                eligible_members.append(family_member)
        
        return [eligible_member.to_dict() for eligible_member in eligible_members] if len(eligible_members) != 0 and eligible_members != [] else None
    
    def evaluateYoloGstGrant(self):
        if self.household_type != "HDB":
            return None
        income = 0
        for family_member in self.family_members:
            income += family_member.annual_income
        
        return [family_member.to_dict() for family_member in self.family_members] if income < 100000 else None
    
    def getEligibleGrants(self,result):
        #Student Encouragement Bonus
        student_encouragement_qualifiers = self.evaluateStudentEncouragementBonus()
        if student_encouragement_qualifiers != None:
            result["student_encouragement_bonus"][self.household_id] = student_encouragement_qualifiers
            
        #Multigeneration Scheme 
        multigeneration_scheme_qualifiers = self.evaluateMultiGenerationScheme()
        if multigeneration_scheme_qualifiers != None:
            result["multigeneration_scheme"][self.household_id] = multigeneration_scheme_qualifiers
            
        #Elder Bonus
        elder_bonus_qualifiers = self.evaluateElderBonus()
        if elder_bonus_qualifiers != None:
            result["elder_bonus"][self.household_id] = elder_bonus_qualifiers
            
        #Baby Sunshine Grant 
        baby_sunshine_grant_qualifiers = self.evaluateBabySunshineGrant()
        if baby_sunshine_grant_qualifiers != None:
            result["baby_sunshine_grant"][self.household_id] = baby_sunshine_grant_qualifiers
            
        #YOLO GST Grant 
        yolo_gst_grant_qualifiers = self.evaluateYoloGstGrant()
        if yolo_gst_grant_qualifiers != None:
            result["yolo_gst_grant"][self.household_id] = yolo_gst_grant_qualifiers