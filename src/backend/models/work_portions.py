from db import db

class WorkDetailsModel(db.Model):
    __tablename__ = 'work_details'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80))
    subcategory = db.Column(db.String(80))
    specification = db.Column(db.String(80))
    start_datetime = db.Column(db.Float(precision=0))
    end_datetime = db.Column(db.Float(precision=0))
    remarks = db.Column(db.String(80))

    def __init__(self, category, subcategory, specification, start_timestamp, end_timestamp, remarks):
        self.category = category
        self.subcategory = subcategory
        self.specification = specification
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.remarks = remarks

    def json(self):
        return {
            'id': self.id,
            'category': self.category,
            'subcategory': self.subcategory,
            'specification': self.specification,
            'start_datetime': self.start_datetime,
            'end_datetime': self.end_datetime,
            'remarks': self.remarks,
        }

    @classmethod
    def find_by_id(cls, id):
        """
        is deze functie nodig of heeft sqlalchemy daar een directe methode voor?
        """
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_time_and_category(cls, category, subcategory, specification, start_timestamp, end_timestamp):
        if category=="":
            return cls.query.filter_by(
                start_datetime=start_timestamp,
                end_datetime=end_timestamp
            ).all()
        elif subcategory=="":
            return cls.query.filter_by(
                category=category,
                start_datetime=start_timestamp,
                end_datetime=end_timestamp
            ).all()
        elif specification=="":
            return cls.query.filter_by(
                category=category,
                subcategory=subcategory,
                start_datetime=start_timestamp,
                end_datetime=end_timestamp
            ).all()
        else:
            return cls.query.filter_by(
                category=category,
                subcategory=subcategory,
                specification=specification,
                start_datetime=start_timestamp,
                end_datetime=end_timestamp
            ).all()

    @classmethod
    def find_by_category(cls, category, subcategory, specification):
        if category=="":
            return cls.query.filter_by(
            ).all()
        elif subcategory=="":
            return cls.query.filter_by(
                category=category
            ).all()
        elif specification=="":
            return cls.query.filter_by(
                category=category,
                subcategory=subcategory
            ).all()
        else:
            return cls.query.filter_by(
                category=category,
                subcategory=subcategory,
                specification=specification
            ).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
