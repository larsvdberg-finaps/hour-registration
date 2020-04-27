from db import db
from helpers.misc import timestamp_to_string


class WorkTypesModel(db.Model):
    __tablename__ = 'work_types'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80))
    subcategory = db.Column(db.String(80))
    specification = db.Column(db.String(80))
    bookmarked = db.Column(db.Boolean)
    last_used = db.Column(db.Float(precision=3))

    def __init__(self, category, subcategory, specification, bookmarked, last_used):
        self.category = category
        self.subcategory = subcategory
        self.specification = specification
        self.bookmarked = bookmarked
        self.last_used = last_used

    def json(self):
        return {
            'category': self.category,
            'subcategory': self.subcategory,
            'specification': self.specification,
            'bookmarked': self.bookmarked,
            'last_used': timestamp_to_string(self.last_used),
        }

    @classmethod
    def find_by_type(cls, category, subcategory, specification):
        return cls.query.filter_by(category=category, subcategory=subcategory, specification=specification).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
