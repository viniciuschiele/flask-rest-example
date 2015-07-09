from marshmallow import Schema
from marshmallow import MarshalResult


class ItemsSchema(Schema):
    def __init__(self, base_schema, items_name='items', count=None):
        super().__init__()
        self.base_schema = base_schema
        self.items_name = items_name
        self.count = count

    def dump(self, obj, many=None, update_fields=True, **kwargs):
        data = self.base_schema.dump(obj, many, update_fields, **kwargs).data
        result = {
            self.items_name: data
        }

        if self.count is not None:
            result['count'] = self.count

        return MarshalResult(result, None)
