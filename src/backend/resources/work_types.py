from flask_restful import Resource, reqparse
from flask import request


class WorkTypes(Resource):
    parser = reqparse.RequestParser()

    def get(self):

        filter = request.args.get('filter', default='all')  # filter can be: all, active, bookmarks

        return {
            "filter": filter,
        }
