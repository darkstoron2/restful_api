import flask
from flask import jsonify, request
from . import db_session
from .jobs import Jobs


blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('user.name', 'job', 'work_size'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_news(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': jobs.to_dict(only=(
                'job', 'work_size', 'user.name', 'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'job', 'team_leader', 'is_finished', 'work_size']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    jobs_all = db_sess.query(Jobs).all()
    if any([request.json['id'] == i.id for i in jobs_all]):
        return jsonify({'error': 'Id already exists'})
    jobs = Jobs(
        id=request.json['id'],
        job=request.json['job'],
        team_leader=request.json['team_leader'],
        is_finished=request.json['is_finished'],
        work_size=request.json['work_size']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})
