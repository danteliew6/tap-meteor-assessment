from src.government_grant import db


class FamilyMember(db.Model):
    # Start of DB model
    __tablename__ = 'family_members'
    __mapper_args__ = {'polymorphic_identity': 'family_members'}
    __table_args__={'mysql_engine':'InnoDB'}


    name = db.Column(db.String(50), primary_key = True)
    gender = db.Column(db.String(20))
    marital_status = db.Column(db.String(20))
    occupation_type = db.Column(db.String(20))
    annual_income = db.Column(db.Float(), default = 0)
    dob =  db.Column(db.Date(), default = 0)
    household_id = db.Column(db.Integer(),db.ForeignKey('households.household_id'))

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