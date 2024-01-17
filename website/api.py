from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from .models import Teacher, Contact, Tag
from . import db
import uuid

def generate_uuid():
    return str(uuid.uuid4())

api = Blueprint('api', __name__)
api_rest = Api(api)

# Přidání parseru pro validaci vstupních dat
parser = reqparse.RequestParser()
parser.add_argument('title_before', type=str)
parser.add_argument('first_name', type=str)
# Přidejte další argumenty podle potřeby

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
        
        args = parser.parse_args()
        provided_uuid = args.get("UUID")
        if not provided_uuid:
            # If UUID is not provided, generate a new one
            provided_uuid = generate_uuid()
        new_teacher = Teacher(
            UUID=provided_uuid,
            title_before=args.get("title_before"),
            first_name=args.get("first_name"),
            middle_name=args.get("middle_name"),
            last_name=args.get("last_name"),
            title_after=args.get("title_after"),
            picture_url=args.get("picture_url"),
            location=args.get("location"),
            claim=args.get("claim"),
            bio=args.get("bio"),
            price_per_hour=args.get("price_per_hour")
        )
        db.session.add(new_teacher)
        db.session.commit()

        tags = [Tag(uuid=tag["uuid"], name=tag["name"]) for tag in args.get("tags", [])]
        new_teacher.tags = tags
        
        

    
       
        telephone_numbers = listToString(args.get("contact", {}).get("telephone_numbers", []))

        emails=listToString(args.get("contact", {}).get("emails", []))
        
        new_contact = Contact(telephone_numbers=telephone_numbers, emails=emails, teacher_id= new_teacher.UUID)
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
