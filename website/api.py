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
    def get(self, uuid):
        teacher = Teacher.query.filter_by(UUID=uuid).first()
        if teacher:
            contact = Contact.query.filter_by(teacher_id=uuid).first()
            tags = Tag.query.filter_by(teacher_id=uuid).all()
            
            # Vytvořte slovník s potřebnými informacemi
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

api_rest.add_resource(LecturerResource, '/lecturer/<uuid>')