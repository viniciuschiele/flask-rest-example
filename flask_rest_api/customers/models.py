from datetime import datetime
from .. import db


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    country_code = db.Column(db.String(2), nullable=False)
    website = db.Column(db.String(100))
    enabled = db.Column(db.Boolean(), nullable=False, default=True)
    updated_at = db.Column(db.DateTime(), nullable=False, default=lambda: datetime.utcnow())
    created_at = db.Column(db.DateTime(), nullable=False, default=lambda: datetime.utcnow())
