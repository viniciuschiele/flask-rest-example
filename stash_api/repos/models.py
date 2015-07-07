from datetime import datetime
from .. import db


class Repository(db.Model):
    __tablename__ = 'repositories'
    __table_args__ = (db.UniqueConstraint('owner_id', 'name'), {'schema': 'repo'})

    id = db.Column(db.BigInteger(), primary_key=True, autoincrement=True)
    owner_id = db.Column(db.BigInteger(), index=True, nullable=False)
    name = db.Column(db.String(100), index=True, nullable=False)
    files = db.relationship('File', lazy='noload')
    created_at = db.Column(db.DateTime(), default=lambda: datetime.utcnow(), nullable=False)
    updated_at = db.Column(db.DateTime(), default=lambda: datetime.utcnow(), nullable=False)

    @staticmethod
    def create(data):
        repo = Repository()
        repo.owner_id = data.get('owner_id')
        repo.name = data.get('name')
        return repo


class File(db.Model):
    __tablename__ = 'files'
    __table_args__ = (db.UniqueConstraint('repository_id', 'path'), {'schema': 'repo'})

    repository_id = db.Column(db.BigInteger, db.ForeignKey('repo.repositories.id', ondelete='cascade'), primary_key=True)
    path = db.Column(db.String(255), primary_key=True)
    content = db.Column(db.Text)
