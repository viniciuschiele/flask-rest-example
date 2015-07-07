from marshmallow import fields
from flask_marshmallow import Schema


class RepositorySchema(Schema):
    id = fields.Integer()
    name = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
