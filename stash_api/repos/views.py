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
from ..common.flask import no_content
from ..common.flask import not_found
from ..common.marshmallow import ItemsSchema

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


@app.route('/<int:id>', methods=['DELETE'])
def delete_repository(id):
    repository = Repository.query.filter_by(id=id).first()
    if not repository:
        return not_found(ResponseError.repository_not_found, id)

    db.session.delete(repository)
    db.session.commit()

    return no_content()


@app.route('/<int:id>', methods=['GET'])
def get_repository(id):
    repository = Repository.query.filter_by(id=id).first()
    if not repository:
        return not_found(ResponseError.repository_not_found, id)

    return content(repository, RepositorySchema())


@app.route('/', methods=['GET'])
def list_repositories():
    repositories = Repository.query.all()
    return content(repositories, ItemsSchema(RepositorySchema(many=True), 'repositories'))
