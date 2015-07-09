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

    def test_delete_repo(self):
        data = dict(owner_id=1, name='test')
        response = self.client.post('/repos', data=json.dumps(data), content_type='application/json')

        repo = json.loads(response.get_data(as_text=True))

        response = self.client.delete('/repos/' + str(repo.get('id')))
        assert response.status_code == 204

    def test_delete_not_existing_repo(self):
        response = self.client.delete('/repos/123123')
        assert response.status_code == 404

    def test_get_repo(self):
        data = dict(owner_id=1, name='test')
        response = self.client.post('/repos', data=json.dumps(data), content_type='application/json')
        repo = json.loads(response.get_data(as_text=True))

        response = self.client.get('/repos/' + str(repo.get('id')))

        assert response.status_code == 200

        repo = json.loads(response.get_data(as_text=True))

        assert repo.get('name') == 'test'

    def test_get_not_existing_repo(self):
        response = self.client.get('/repos/2313231')

        assert response.status_code == 404

    def test_list_repositories(self):
        data = dict(owner_id=1, name='test')
        self.client.post('/repos', data=json.dumps(data), content_type='application/json')

        response = self.client.get('/repos')

        assert response.status_code == 200

        repositories = json.loads(response.get_data(as_text=True)).get('repositories')

        assert len(repositories) == 1
