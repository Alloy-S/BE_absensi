from flask_restful import fields, reqparse

jabatan_pagination_fields = {
    "pages": fields.String,
    "total": fields.String,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'nama': fields.String,
        'parent_name': fields.String
    }))
}

jabatan_fields = {
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'nama': fields.String,
    }))
}

jabatan_field = {
    'id': fields.String,
    'nama': fields.String,
    'parent_id': fields.String
}

pagination_args = reqparse.RequestParser()
pagination_args.add_argument('page', type=int, location="args", default=1)
pagination_args.add_argument('size', type=int, location="args", default=10)
pagination_args.add_argument('search', type=str, location="args", default="")

jabatan_args = reqparse.RequestParser()
jabatan_args.add_argument('nama', type=str, required=True, help="Nama Jabatan cannot be blank")
jabatan_args.add_argument('parent_id', type=str, required=False, help="Parent ID cannot be blank")
