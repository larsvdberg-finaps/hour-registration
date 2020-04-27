from flask_restful import Resource, reqparse


class HomePage(Resource):
    # get part of the list, based on start/end time, (sub)category etc.

    def get(self):
        return {"Homepage": "homepage has not been constructed yet."}
