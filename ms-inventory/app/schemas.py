from marshmallow import Schema, fields

class BrandSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    brand = fields.Str(required=True)
