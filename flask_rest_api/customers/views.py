from flask import Blueprint
from datetime import datetime
from .models import Company
from .schemas import CompanySchema
from .. import db, io

app = Blueprint('companies', __name__, url_prefix='/companies')
  

@app.route('/', methods=['POST'])
@io.from_body('company', CompanySchema)
def add_company(company):
    db.session.add(company)
    db.session.commit()
    return company


@app.route('/<int:id>', methods=['DELETE'])
def delete_company(id):
    company = Company.query.filter_by(id=id).first()

    if not company:
        return io.not_found('Company not found: ' + str(id))

    db.session.delete(company)
    db.session.commit()

    return io.no_content()  # this is optional


@app.route('/<int:id>', methods=['GET'])
@io.marshal_with(CompanySchema)
def get_company(id):
    company = Company.query.filter_by(id=id).first()

    if not company:
        return io.not_found('Company not found: ' + str(id))

    return company


@app.route('/', methods=['GET'])
@io.marshal_with(CompanySchema)
def list_companies():
    return Company.query.all()


@app.route('/<int:id>', methods=['POST', 'PATCH'])
@io.from_body('update_company', CompanySchema)
@io.marshal_with(CompanySchema)
def update_company(id, new_company):
    company = Company.query.filter_by(id=id).first()

    if not company:
        return io.not_found('Company not found: ' + str(id))

    company.name = new_company.name
    company.country_code = new_company.country_code
    company.website = new_company.website
    company.enabled = new_company.enabled
    company.updated_at = datetime.now()

    return company
