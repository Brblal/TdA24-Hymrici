from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from .models import Teacher, Contact, Tag
from . import db

api = Blueprint('api', __name__)
api_rest = Api(api)

# Přidání parseru pro validaci vstupních dat
parser = reqparse.RequestParser()
parser.add_argument('title_before', type=str)
parser.add_argument('first_name', type=str)
# Přidejte další argumenty podle potřeby

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
        args = parser.parse_args()
        new_teacher = Teacher(
            title_before=args['title_before'],
            first_name=args['first_name'],
            # Add other attributes as needed
        )
        db.session.add(new_teacher)
        db.session.commit()

        # Assume you have a function to generate UUID
        new_uuid = generate_uuid()

        new_contact = Contact(
            telephone_numbers="",
            emails="",
            teacher_id=new_uuid
        )
        db.session.add(new_contact)
        db.session.commit()

        return {'message': 'Lecturer created successfully'}, 201

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

api_rest.add_resource(LecturerResource, '/lecturer', '/lecturer/<uuid>')

