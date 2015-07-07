from flask import Blueprint
from flask_binding import bind
from flask_binding import FromBody
from .models import Repository
from .schemas import RepositorySchema
from .. import db

app = Blueprint('repos', __name__, url_prefix='/repos')
  
  
@app.route('/', methods=['POST'])
@bind({'repo_data': FromBody(dict, required=True)})
def create_repo(repo_data):
    repo = Repository.create(repo_data)

    db.session.add(repo)
    db.session.commit()

    return RepositorySchema().jsonify(repo)


@app.route('/', methods=['GET'])
def list_repos():
    return Repository.query.all()
