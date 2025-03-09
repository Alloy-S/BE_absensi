from flask_restful import fields, reqparse

lokasi_args = reqparse.RequestParser()
lokasi_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
lokasi_args.add_argument('longitude', type=float, required=True, help="longitude cannot be blank")
lokasi_args.add_argument('latitude', type=float, required=True, help="latitude cannot be blank")
lokasi_args.add_argument('toleransi', type=int, required=True, help="waktu toleransi cannot be blank")


lokasi_fields = {
    'id': fields.String,
    'name': fields.String,
    'longitude': fields.Float,
    'latitude': fields.Float,
    'toleransi' : fields.Integer
}