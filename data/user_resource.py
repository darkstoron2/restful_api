from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument('surname', required=False)
parser.add_argument('name', required=False)
parser.add_argument('age', required=False, type=int)
parser.add_argument('position', required=False, type=int)
parser.add_argument('speciality', required=False, type=int)
parser.add_argument('address', required=False, type=int)
parser.add_argument('email', required=False)
parser.add_argument('password', required=False)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"user {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('surname', 'name', 'age', 'email'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        args = parser.parse_args()
        user.name = args['name'] if args['name'] is not None else user.name
        user.surname = args['surname'] if args['surname'] is not None else user.surname
        user.age = args['age'] if args['age'] is not None else user.age
        user.email = args['email'] if args['email'] is not None else user.email
        user.position = args['position'] if args['position'] is not None else user.position
        user.speciality = args['speciality'] if args['speciality'] is not None else user.speciality
        user.address = args['address'] if args['address'] is not None else user.address
        user.email = args['email'] if args['email'] is not None else user.email
        if args['password'] is not None:
            user.set_password(args['password'])
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'user': [item.to_dict(
            only=('surname', 'name', 'age')) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if not all(args[key] is not None for key in ['name', 'surname', 'age', 'email', 'password']):
            abort(404, message=f"Not all keys")
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email']
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})