from flask_restful import fields, reqparse
from utils.args_date import valid_time_no_second

jadwal_args = reqparse.RequestParser()
jadwal_args.add_argument('shift', type=str, required=True, help="Shift cannot be blank")
jadwal_args.add_argument('time_in', type=valid_time_no_second, required=True)
jadwal_args.add_argument('time_out', type=valid_time_no_second, required=True)
jadwal_args.add_argument('toler_in', type=int, required=True, help="Toler In cannot be blank")
jadwal_args.add_argument('toler_out', type=int, required=True, help="Toler Out cannot be blank")


jadwal_fields = {
    'id': fields.String,
    'shift': fields.String,
    'time_in': fields.String,
    'time_out': fields.String,
    'toler_in': fields.Integer,
    'toler_out': fields.Integer
}