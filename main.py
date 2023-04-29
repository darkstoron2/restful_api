from flask import Flask
from flask_restful import Api

from data import db_session
from data.jobs_resource import JobsListResource, JobsResource
from data.user_resource import UserListResource, UserResource
from flask_login import LoginManager


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    api.add_resource(UserListResource, '/api/v2/user')
    api.add_resource(UserResource, '/api/v2/user/<int:user_id>')
    api.add_resource(JobsListResource, '/api/v2/jobs')
    api.add_resource(JobsResource, '/api/v2/jobs/<int:jobs_id>')
    db_session.global_init("db/mars_explorer.db")
    app.run()


if __name__ == '__main__':
    main()
