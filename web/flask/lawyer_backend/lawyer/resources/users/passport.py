from flask_restful import Resource


class NewClientResource(Resource):
    def get(self):
        return {"name": "xf"}


class AuthorizationResource(Resource):
    pass
