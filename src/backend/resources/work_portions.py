from flask_restful import Resource, reqparse
from flask import request


class WorkPortion(Resource):
    # post a new one
    # get one, by id
    # update one, by id
    # delete one, by id
    parser = reqparse.RequestParser()

    def get(self, id):
        return {"id": id}


class WorkPortions(Resource):
    # get part of the list, based on start/end time, (sub)category etc.

    def get(self):

        category = request.args.get('category')
        subcategory = request.args.get('subcategory')
        specification = request.args.get('specification')
        earliest = request.args.get('earliest', type = int)
        latest = request.args.get('latest', type = int)

        return {
            "category": category,
            "subcategory": subcategory,
            "specification": specification,
            "earliest": earliest,
            "latest": latest
        }
