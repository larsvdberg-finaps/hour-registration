import os

from flask import Flask
from flask_restful import Api

from resources.work_portions import WorkPortion, WorkPortions
from resources.work_types import WorkTypes
from resources.homepage import HomePage

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

api.add_resource(WorkPortion, '/workportion/<int:id>')
api.add_resource(WorkPortions, '/workportions')
api.add_resource(WorkTypes, '/worktypes')

# remove later when we have a frontend
api.add_resource(HomePage, '/')


if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5005)
