from marshmallow import Schema, fields, validate, ValidationError

class AccountSchema(Schema):
    fullname = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)

class PersonalSchema(Schema):
    gender = fields.String(required=True)
    birth_place = fields.String(required=True)
    birth_date = fields.String(required=True)
    marital_status = fields.String(required=True)
    religion = fields.String(required=True)
    blood_type = fields.String(required=True)

class ContactSchema(Schema):
    phone = fields.String(required=True)
    address = fields.String(required=True)
    country = fields.String(required=True)
    province = fields.String(required=True)
    city = fields.String(required=True)

class EmployeeSchema(Schema):
    nip = fields.String(required=True)
    position = fields.String(required=True)
    division = fields.String(required=True)
    work_location = fields.String(required=True)
    employment_status = fields.String(required=True)

class UserSchema(Schema):
    account = fields.Nested(AccountSchema, required=True)
    personal = fields.Nested(PersonalSchema, required=True)
    contact = fields.Nested(ContactSchema, required=True)
    employee = fields.Nested(EmployeeSchema, required=True)

class RootSchema(Schema):
    user = fields.Nested(UserSchema, required=True)

