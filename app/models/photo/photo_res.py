from flask_restful import fields

photo_field = {
    "id": fields.String,
    "filename": fields.String,
    "type": fields.String,
    "mimetype": fields.String,
    "image": fields.String,
}
