from flask import jsonify


def conflict(error, *args):
    message = error.value % args
    response = jsonify(error=dict(code=error.name, message=message))
    response.status_code = 409
    return response


def content(obj, schema=None):
    if schema:
        obj = schema.dump(obj).data
    return jsonify(obj)
