from flask import Blueprint
from flask_binding import bind
from flask_binding import FromBody
from sqlalchemy.exc import IntegrityError
from .enums import ResponseError
from .models import Repository
from .schemas import RepositorySchema
from .. import db
from ..common.flask import conflict
from ..common.flask import content

app = Blueprint('repos', __name__, url_prefix='/repos')
  
  
@app.route('/', methods=['POST'])
@bind({'data': FromBody(dict, required=True)})
def create_repository(data):
    repository = Repository.create(data)

    try:
        db.session.add(repository)
        db.session.commit()
    except IntegrityError as e:
        if 'duplicate key' in str(e):
            return conflict(ResponseError.repository_already_exists, repository.name)
        raise

    return content(repository, RepositorySchema())


@app.route('/', methods=['GET'])
def list_repositories():
    repositories = Repository.query.all()
    return content(repositories, RepositorySchema(many=True))
