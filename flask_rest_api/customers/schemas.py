from flask_io import fields, Schema, post_dump
from .models import Company


class CompanySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    country_code = fields.String(required=True)
    website = fields.String(allow_none=True)
    enabled = fields.Boolean(required=True)
    updated_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    @post_dump
    def make_object(self, data):
        return Company(**data)
