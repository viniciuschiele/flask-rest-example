import json

from flask_rest_api import db
from flask_rest_api.application import create_app
from unittest import TestCase


class TestView(TestCase):
    def setUp(self):
        self.app = create_app('development')
        self.client = self.app.test_client()
        db.create_all(app=self.app)

    def tearDown(self):
        db.session.remove()
        db.drop_all(app=self.app)

    def test_create_company(self):
        data = dict(name='test', country_code='IE', website='http://example.com', enabled=True)
        response = self.client.post('/companies', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200

    def test_delete_company(self):
        data = dict(name='test', country_code='IE', website='http://example.com', enabled=True)
        response = self.client.post('/companies', data=json.dumps(data), content_type='application/json')

        company = json.loads(response.get_data(as_text=True))

        response = self.client.delete('/companies/' + str(company.get('id')))
        assert response.status_code == 204

    def test_delete_not_existing_company(self):
        response = self.client.delete('/companies/99999')
        assert response.status_code == 404

    def test_get_company(self):
        data = dict(name='test', country_code='IE', website='http://example.com', enabled=True)
        response = self.client.post('/companies', data=json.dumps(data), content_type='application/json')
        company = json.loads(response.get_data(as_text=True))

        response = self.client.get('/companies/' + str(company.get('id')))

        assert response.status_code == 200

        company = json.loads(response.get_data(as_text=True))

        assert company.get('name') == 'test'

    def test_get_not_existing_company(self):
        response = self.client.get('/companies/99999')

        assert response.status_code == 404

    def test_list_companies(self):
        data = dict(name='test', country_code='IE', website='http://example.com', enabled=True)
        self.client.post('/companies', data=json.dumps(data), content_type='application/json')

        response = self.client.get('/companies')

        assert response.status_code == 200

        companies = json.loads(response.get_data(as_text=True))

        assert len(companies) == 1
