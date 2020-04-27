from flask_restful import Resource, reqparse
from flask import request
from datetime import datetime
from helpers.misc import timestamp_to_string

from models.work_types import WorkTypesModel


class WorkTypes(Resource):
    def get(self):

        bookmarked = request.args.get('bookmarked', type=bool, default=False)
        max_idle_time = request.args.get('max_idle_time', type=int)

        if max_idle_time is not None:
            current_timestamp = datetime.now().timestamp()
            oldest_allowed_timestamp = current_timestamp - max_idle_time
            oldest_allowed_timestring = timestamp_to_string(oldest_allowed_timestamp)
            if bookmarked:
                return {f'bookmarked work types, used after {oldest_allowed_timestring}': [
                    x.json() for x in WorkTypesModel.query.filter(
                        WorkTypesModel.bookmarked == True, WorkTypesModel.last_used >= oldest_allowed_timestamp
                    ).all()
                ]}
            else:
                return {f'all work types, used after {oldest_allowed_timestring}': [
                    x.json() for x in WorkTypesModel.query.filter(
                        WorkTypesModel.last_used >= oldest_allowed_timestamp
                    ).all()
                ]}
        else:
            if bookmarked:
                return {'bookmarked work types': [x.json() for x in WorkTypesModel.query.filter_by(bookmarked=True).all()]}
            else:
                return {'all work types': [x.json() for x in WorkTypesModel.query.all()]}

    def delete(self):
        # TODO: add feature to delete only a selection, like the non-bookmarked ones or the really old ones
        for worktype in WorkTypesModel.query.all():
            worktype.delete_from_db()



class WorkType(Resource):
    parser = reqparse.RequestParser()
    help_msg = "The argument `{}` should not be blank."
    parser.add_argument('category', type=str, required=True, help=help_msg.format('category'))
    parser.add_argument('subcategory', type=str, required=True, help=help_msg.format('subcategory'))
    parser.add_argument('specification', type=str, required=True,  help=help_msg.format('specification'))
    parser.add_argument('bookmarked', type=bool, required=False)
    parser.add_argument('last_used', type=float, required=False)


    def get(self):
        category = request.args.get('category')
        subcategory = request.args.get('subcategory')
        specification = request.args.get('specification')

        worktype = WorkTypesModel.find_by_type(category, subcategory, specification)
        if worktype is not None:
            return worktype.json()
        else:
            return {'error': "work type '{} - {} - {}' not found".format(
                category, subcategory, specification
            )}, 404


    def post(self):
        current_timestamp = datetime.now().timestamp()

        data = WorkType.parser.parse_args()
        data['last_used'] =  current_timestamp  # last_used is always the current time at a post request
        if data['bookmarked'] == None: data['bookmarked'] = True  # bookmarked by default

        category = data['category']
        subcategory = data['subcategory']
        specification = data['specification']

        if WorkTypesModel.find_by_type(category, subcategory, specification) is not None:
            return {'message': "The work type '{} - {} - {}' already exists.".format(
                category, subcategory, specification
            )}, 400

        worktype = WorkTypesModel(**data)
        try:
            worktype.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return worktype.json(), 201


    def put(self):
        #  Old values in url query params, new values in parser arguments

        old_category = request.args.get('category')
        old_subcategory = request.args.get('subcategory')
        old_specification = request.args.get('specification')

        new_data = WorkType.parser.parse_args()

        new_category = new_data['category']
        new_subcategory = new_data['subcategory']
        new_specification = new_data['specification']

        worktype = WorkTypesModel.find_by_type(old_category, old_subcategory, old_specification)
        wanted_worktype = WorkTypesModel.find_by_type(new_category, new_subcategory, new_specification)

        if wanted_worktype not in [None, worktype]:
            return {"error": "put request failed: it would result in duplicate worktypes",
                    "retained item to be updated": worktype.json(),
                    "retained item that would be overwritten": wanted_worktype.json(),
            }, 400

        # update worktype with new_data
        if worktype is None:
            #  nothing to replace, `put` amounts to `post` in this case. Create new `worktype`.
            old_data = "None"
            if new_data['bookmarked'] is None: new_data['bookmarked'] = True
            if new_data['last_used'] is None: new_data['last_used'] = datetime.now().timestamp()
            worktype = WorkTypesModel(**new_data)
        else:
            #  replace data in old_worktype by new values that are not None or "None"
            old_data = worktype.json()
            if new_data['category'] is not "None": worktype.category = new_data['category']
            if new_data['subcategory'] is not "None": worktype.subcategory = new_data['subcategory']
            if new_data['specification'] is not "None": worktype.specification = new_data['specification']
            if new_data['bookmarked'] is not None: worktype.bookmarked = new_data['bookmarked']
            if new_data['last_used'] is not None: worktype.last_used = new_data['last_used']

        try:
            worktype.save_to_db()
            new_data = worktype.json()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return {"old values": old_data, "new values": new_data}


    def delete(self):
        category = request.args.get('category')
        subcategory = request.args.get('subcategory')
        specification = request.args.get('specification')

        worktype = WorkTypesModel.find_by_type(category, subcategory, specification)
        if worktype is not None:
            worktype.delete_from_db()
            return {'message': 'Item deleted', 'item': worktype.json()}
        else:
            return {'error': "work type '{} - {} - {}' not found".format(
                category, subcategory, specification
            )}, 400

