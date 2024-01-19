from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask_restful import Api, Resource, reqparse
from .models import Teacher, Contact, Tag
from . import db
import uuid
import json
from uuid import UUID
from collections import OrderedDict
from flask import Flask, Response, json
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

class CustomJSONEncoder(json.JSONEncoder):
    def encode(self, obj):
        if isinstance(obj, OrderedDict):
            return super(CustomJSONEncoder, self).encode(list(obj.items()))
        return super(CustomJSONEncoder, self).encode(obj)

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
        parser.add_argument('first_name', type=str, required=False)
        parser.add_argument('last_name', type=str, required=False)
        parser.add_argument('uuid', type=str, required=False)
        parser.add_argument('middle_name', type=str, required=False)
        parser.add_argument('title_before', type=str, required=False)
        parser.add_argument('title_after', type=str, required=False)
        parser.add_argument('picture_url', type=str, required=False)
        parser.add_argument('location', type=str, required=False)
        parser.add_argument('claim', type=str, required=False)
        parser.add_argument('bio', type=str, required=False)
        parser.add_argument('price_per_hour', type=int, required=False)
        
        parser.add_argument('contact', type=dict, required=False)
        
        parser.add_argument('tags', type=list, required=False, location='json')
        

        args = parser.parse_args()
        # Extract and validate tags
        tags = args.get("tags", [])

        

   
            
        
        
        telephone_numbers = str(args['contact']['telephone_numbers'])
        emails = str(args['contact']['emails'])
        uuid_str = str(args['uuid'])
        
        lecturer = Teacher(title_before = args['title_before'], first_name=args['first_name'], middle_name = args['middle_name'] , last_name=args['last_name'], title_after = args['title_after'] , picture_url = args['picture_url'], location = args['location'] , claim = args['claim'] , bio = args['bio'] , price_per_hour = args['price_per_hour'] , UUID=uuid_str)
        
        
        db.session.add(lecturer)
        db.session.commit()
        if tags is not None:
            tag_objects = []
            for tag in tags:
                if isinstance(tag, dict) and 'uuid' in tag and 'name' in tag:
                    existing_tag = Tag.query.filter_by(uuid=tag["uuid"]).first()
                    if existing_tag:
                        # Update the existing tag with the new lecturer's UUID
                        existing_tag.teacher_id = lecturer.UUID
                        tag_objects.append(existing_tag)
                    else:
                        tag_objects.append(Tag(uuid=tag["uuid"], name=tag["name"], teacher_id=lecturer.UUID))
                
        
        
            
            db.session.add_all(tag_objects)
            db.session.commit()
        contact = Contact(telephone_numbers = telephone_numbers, emails = emails, teacher_id = lecturer.UUID)
        db.session.add(contact)
        db.session.commit()
        
        
        
        tags_response = [{"uuid": tag.uuid, "name": tag.name} for tag in tag_objects] if tags else []
        response_data = OrderedDict({
            "first_name": lecturer.first_name,
            "last_name": lecturer.last_name,
            "uuid": str(lecturer.UUID),
            "title_before": lecturer.title_before,
            "middle_name": lecturer.middle_name,
            "title_after": lecturer.title_after,
            "picture_url": lecturer.picture_url,
            "location": lecturer.location,
            "claim": lecturer.claim,
            "bio": lecturer.bio,
            "tags": tags_response,  # Use the ordered list of tags
            "price_per_hour": lecturer.price_per_hour,
            "contact": {
                "telephone_numbers": contact.telephone_numbers,
                "emails": contact.emails
            }
            })


       

        json_str = json.dumps(response_data, indent=2, ensure_ascii=False, sort_keys=False)
        response = Response(json_str, content_type='application/json; charset=utf-8')
        
        return response


    def put(self, uuid):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=False)
        parser.add_argument('last_name', type=str, required=False)
        parser.add_argument('middle_name', type=str, required=False)
        parser.add_argument('title_before', type=str, required=False)
        parser.add_argument('title_after', type=str, required=False)
        parser.add_argument('picture_url', type=str, required=False)
        parser.add_argument('location', type=str, required=False)
        parser.add_argument('claim', type=str, required=False)
        parser.add_argument('bio', type=str, required=False)
        parser.add_argument('price_per_hour', type=int, required=False)
        parser.add_argument('contact', type=dict, required=False)
        parser.add_argument('tags', type=list, required=False, location='json')

        args = parser.parse_args()
        teacher = Teacher.query.filter_by(UUID=uuid).first()

        if teacher:
            # Update teacher attributes
            teacher.title_before = args['title_before']
            teacher.first_name = args['first_name']
            teacher.middle_name = args['middle_name']
            teacher.last_name = args['last_name']
            teacher.title_after = args['title_after']
            teacher.picture_url = args['picture_url']
            teacher.location = args['location']
            teacher.claim = args['claim']
            teacher.bio = args['bio']
            teacher.price_per_hour = args['price_per_hour']

            # Update contact information
            contact = Contact.query.filter_by(teacher_id=uuid).first()
            if contact:
                contact.telephone_numbers = str(args['contact']['telephone_numbers'])
                contact.emails = str(args['contact']['emails'])
            
            # Update tags
            tags = args.get("tags", [])
            if tags:
                tag_objects = []
                for tag in tags:
                    if isinstance(tag, dict) and 'uuid' in tag and 'name' in tag:
                        existing_tag = Tag.query.filter_by(uuid=tag["uuid"]).first()
                        if existing_tag:
                            existing_tag.teacher_id = teacher.UUID
                            tag_objects.append(existing_tag)
                        else:
                            tag_objects.append(Tag(uuid=tag["uuid"], name=tag["name"], teacher_id=teacher.UUID))

                db.session.add_all(tag_objects)

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
