from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.jobs import Jobs
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument('team_leader', required=False, type=int)
parser.add_argument('job', required=False)
parser.add_argument('work_size', required=False, type=int)
parser.add_argument('collaborators', required=False)
parser.add_argument('is_finished', required=False, type=bool)


def abort_if_jobs_not_found(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        abort(404, message=f"jobs {jobs_id} not found")


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"user {user_id} not found")


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        return jsonify({'jobs': jobs.to_dict(
            only=('job', 'team_leader.name', 'is_finished'))})

    def delete(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        session.delete(jobs)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        args = parser.parse_args()
        jobs.job = args['job'] if args['job'] is not None else jobs.job
        jobs.team_leader = args['team_leader'] if args['team_leader'] is not None else jobs.team_leader
        jobs.work_size = args['work_size'] if args['work_size'] is not None else jobs.work_size
        jobs.collaborators = args['collaborators'] if args['collaborators'] is not None else jobs.collaborators
        jobs.is_finished = args['is_finished'] if args['is_finished'] is not None else jobs.is_finished
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('job', 'team_leader.name', 'is_finished')) for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if not all(args[key] is not None for key in ['job', 'team_leader', 'work_size', 'is_finished']):
            abort(404, message=f"Not all keys")
        abort_if_user_not_found(args['team_leader'])
        jobs = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished']
        )
        session.add(jobs)
        session.commit()
        return jsonify({'success': 'OK'})