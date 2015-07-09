import json

from stash_api import db
from stash_api.app import create_app
from unittest import TestCase


class TestView(TestCase):
    def setUp(self):
        self.app = create_app('development')
        self.client = self.app.test_client()
        db.create_all(app=self.app)

    def tearDown(self):
        db.session.remove()
        db.drop_all(app=self.app)

    def test_create_repo(self):
        data = dict(owner_id=1, name='test')
        response = self.client.post('/repos', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200

    def test_create_duplicated_repo(self):
        data = dict(owner_id=1, name='test')
        response = self.client.post('/repos', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200

        response = self.client.post('/repos', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 409
