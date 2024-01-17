# app/routes.py
from flask import jsonify
from flask_restful import Api, Resource, reqparse
from app.models import Teacher, db

api = Api(app)

class LecturersResource(Resource):
    def get(self):
        lecturers = Teacher.query.all()
        return jsonify([{ "first_name": lecturer.first_name, "last_name": lecturer.last_name, "UUID": lecturer.UUID} for lecturer in lecturers])


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('UUID', type=str, required=True)

        args = parser.parse_args()

        lecturer = Teacher(first_name=args['first_name'], last_name=args['last_name'], UUID=args['UUID'])
        db.session.add(lecturer)
        db.session.commit()

        return jsonify({"first_name": lecturer.first_name, "last_name": lecturer.last_name, "UUID": lecturer.UUID}), 201


api.add_resource(LecturersResource, '/lecturers')