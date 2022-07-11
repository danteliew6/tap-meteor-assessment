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
            if family_member.occupation_type == "student":
                eligible_members.append(family_member)
        
        return [members.to_dict() for members in eligible_members] if income < 200000 else None
        
    def evaluateMultiGenerationScheme(self):
        age_criteria = False
        income = 0
        for family_member in self.family_members:
            income += family_member.annual_income
            age = family_member.getAge()
            if age < 18 or age > 55:
                age_criteria = True
        
        return [family_member.to_dict() for family_member in self.family_members] if income < 150000 and age_criteria else None
    
    # def evaluateElderBonus(self, result):
    #     age_criteria = False
    #     income = 0
    #     for family_member in self.family_members:
    #         income += family_member.annual_income
    #         age = family_member.getAge()
    #         if age < 18 or age > 55:
    #             age_criteria = True
        
    #     return self.family_members if income < 150000 and age_criteria else None
    
    def getEligibleGrants(self,result):
        student_encouragement_qualifiers = self.evaluateStudentEncouragementBonus()
        if student_encouragement_qualifiers != None:
            result["student_encouragement_bonus"].extend(student_encouragement_qualifiers)
        multigeneration_scheme_qualifiers = self.evaluateMultiGenerationScheme()
        if multigeneration_scheme_qualifiers != None:
            result["multigeneration_scheme_qualifiers"].extend(multigeneration_scheme_qualifiers)
            