from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask_restful import Api, Resource, reqparse
from .models import Teacher, Contact, Tag
from . import db
import uuid
from uuid import UUID

def generate_uuid():
    return str(uuid.uuid4())

api = Blueprint('api', __name__)
api_rest = Api(api)



def listToString(s):
 
    # initialize an empty string
    str1 = " "
 
    # return string
    return (str1.join(s))
import uuid



class LecturerResource(Resource):
    def get(self, uuid=None):
        if uuid:
            # Handle GET request for a specific lecturer
            teacher = Teacher.query.filter_by(UUID=uuid).first()
            if teacher:
                contact = Contact.query.filter_by(teacher_id=uuid).first()
                tags = Tag.query.filter_by(teacher_id=uuid).all()

                lecturer_data = {
                    'UUID': teacher.UUID,
                    'title_before': teacher.title_before,
                    'first_name': teacher.first_name,
                    'middle_name': teacher.middle_name,
                    'last_name': teacher.last_name,
                    'title_after': teacher.title_after,
                    'picture_url': teacher.picture_url,
                    'location': teacher.location,
                    'claim': teacher.claim,
                    'bio': teacher.bio,
                    'price_per_hour': teacher.price_per_hour,
                    'telephone_numbers': contact.telephone_numbers,
                    'emails': contact.emails,
                    'tags': [tag.name for tag in tags]
                }

                return lecturer_data, 200
            else:
                return {'message': 'Lecturer not found'}, 404
        else:
            # Handle GET request for all lecturers
            teachers = Teacher.query.all()
            lecturer_list = []

            for teacher in teachers:
                contact = Contact.query.filter_by(teacher_id=teacher.UUID).first()
                tags = Tag.query.filter_by(teacher_id=teacher.UUID).all()

                lecturer_data = {
                    'UUID': teacher.UUID,
                    'title_before': teacher.title_before,
                    'first_name': teacher.first_name,
                    'middle_name': teacher.middle_name,
                    'last_name': teacher.last_name,
                    'title_after': teacher.title_after,
                    'picture_url': teacher.picture_url,
                    'location': teacher.location,
                    'claim': teacher.claim,
                    'bio': teacher.bio,
                    'price_per_hour': teacher.price_per_hour,
                    'telephone_numbers': contact.telephone_numbers,
                    'emails': contact.emails,
                    'tags': [tag.name for tag in tags]
                }

                lecturer_list.append(lecturer_data)

            return lecturer_list, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('uuid', type=str, required=True)
        parser.add_argument('middle_name', type=str, required=True)
        parser.add_argument('title_before', type=str, required=True)
        parser.add_argument('title_after', type=str, required=True)
        parser.add_argument('picture_url', type=str, required=True)
        parser.add_argument('location', type=str, required=True)
        parser.add_argument('claim', type=str, required=True)
        parser.add_argument('bio', type=str, required=True)
        parser.add_argument('price_per_hour', type=int, required=True)
        
        parser.add_argument('contact', type=dict, required=True)
        
        parser.add_argument('tags', type=list, required=False, location='json')
        

        args = parser.parse_args()
        # Extract and validate tags
        tags = args.get("tags", [])

        

        tag_objects = []
        for tag in tags:
            if isinstance(tag, dict) and 'uuid' in tag and 'name' in tag:
                tag_objects.append(Tag(uuid=tag["uuid"], name=tag["name"]))
            else:
                return {'message': 'Each tag must be a dictionary with "uuid" and "name" keys'}, 400

        
        telephone_numbers = str(args['contact']['telephone_numbers'])
        emails = str(args['contact']['emails'])
        uuid_str = str(args['uuid'])
        
        lecturer = Teacher(title_before = args['title_before'], first_name=args['first_name'], middle_name = args['middle_name'] , last_name=args['last_name'], title_after = args['title_after'] , picture_url = args['picture_url'], location = args['location'] , claim = args['claim'] , bio = args['bio'] , price_per_hour = args['price_per_hour'] , UUID=uuid_str)
        
        
        db.session.add(lecturer)
        db.session.commit()
        
        
        
        contact = Contact(telephone_numbers = telephone_numbers, emails = emails, teacher_id = lecturer.UUID)
        db.session.add(contact)
        db.session.commit()
        tag_objects = [Tag(uuid=tag["uuid"], name=tag["name"], teacher_id=lecturer.UUID) for tag in args.get("tags", [])]
        db.session.add_all(tag_objects)
        db.session.commit()
        
        response_data = {
            "first_name": lecturer.first_name,
            "last_name": lecturer.last_name,
            "UUID": str(lecturer.UUID)
            
        }

        # Explicitly create a Flask Response
        response = make_response(jsonify(response_data), 201)
        
        return response


    def put(self, uuid):
        args = parser.parse_args()
        teacher = Teacher.query.filter_by(UUID=uuid).first()

        if teacher:
            teacher.title_before = args['title_before']
            teacher.first_name = args['first_name']
            # Update other attributes as needed

            db.session.commit()

            return {'message': 'Lecturer updated successfully'}, 200
        else:
            return {'message': 'Lecturer not found'}, 404
    def delete(self, uuid=None):
        if uuid:
            # Handle DELETE request for a specific lecturer
            teacher = Teacher.query.filter_by(UUID=uuid).first()

            if teacher:
                db.session.delete(teacher)
                db.session.commit()
                return {'message': 'Lecturer deleted successfully'}, 200
            else:
                return {'message': 'Lecturer not found'}, 404
        else:
            # Handle DELETE request without a specific UUID
            # This is just an example; you can modify the behavior based on your requirements
            # Delete all lecturers (or specify a different behavior)
            teachers = Teacher.query.all()

            for teacher in teachers:
                db.session.delete(teacher)

            db.session.commit()
            
            return {'message': 'All lecturers deleted successfully'}, 200

api_rest.add_resource(LecturerResource, '/lecturers', '/lecturers/<uuid>')
