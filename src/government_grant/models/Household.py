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