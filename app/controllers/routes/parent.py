from app.model.entity.parents import Parents as ParentsEntity
from flask import Blueprint, request, Response
from app.model.extensions.database import mongo
from flask_restx import Namespace, Resource
from http import HTTPStatus

parents = Blueprint('routeParents', __name__)
parents_ns = Namespace('parentsView', validate=True)
parents_ns.model(ParentsEntity.__name__, ParentsEntity.get_parents_model())

#( 'Parents', { 'name': 'string', 'email': 'string', 'phone': 'string', 'created_at': 'string', 'updated_at': 'string' } )

@parents_ns.route('/parents', endpoint='parents')
@parents_ns.response( int(HTTPStatus.BAD_REQUEST), 'Validation erro.' )
@parents_ns.response( int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.' )
class Parents(Resource):
    @parents_ns.response( int(HTTPStatus.OK), 'Success' )
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass