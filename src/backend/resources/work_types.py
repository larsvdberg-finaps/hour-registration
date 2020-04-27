from flask_restful import Resource, reqparse
from flask import request
from datetime import datetime

from models.work_types import WorkTypesModel


class WorkTypes(Resource):
    def get(self):

        active = request.args.get('active')
        bookmarked = request.args.get('bookmarked')
        max_age = request.args.get('max_age')

        return {'all work types': [x.json() for x in WorkTypesModel.query.all()]}


class WorkType(Resource):
    parser = reqparse.RequestParser()
    help_msg = "The argument `{}` should not be blank."
    parser.add_argument('category',
                        type=str,
                        required=True,
                        help=help_msg.format('category')
                        )
    parser.add_argument('subcategory',
                        type=str,
                        required=True,
                        help=help_msg.format('subcategory')
                        )
    parser.add_argument('specification',
                        type=str,
                        required=True,
                        help=help_msg.format('specification')
                        )
    parser.add_argument('active',
                        type=bool,
                        required=True,
                        help=help_msg.format('active')
                        )
    parser.add_argument('bookmarked',
                        type=bool,
                        required=True,
                        help=help_msg.format('bookmarked')
                        )
    def get(self):
        return {'message': 'not implemented yet'}

    def post(self):
        data = WorkType.parser.parse_args()
        current_timestamp = datetime.now().timestamp()

        category = data['category']
        subcategory = data['subcategory']
        specification = data['specification']

        if WorkTypesModel.find_by_type(category, subcategory, specification):
            return {'message': "The work type '{} - {} - {}' already exists.".format(
                category, subcategory, specification
            )}, 400

        worktype = WorkTypesModel(last_used=current_timestamp, **data)
        try:
            worktype.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return worktype.json(), 201
