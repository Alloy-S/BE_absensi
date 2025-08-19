from app.models.payroll.payroll_req import PayrollReq
from flask import request, Blueprint
from flask_restful import Resource, Api, marshal
from app.filter.jwt_filter import role_required, permission_required
from app.models.payroll.payroll_res import rincian_perhitung_field, hasil_penggajian_field, proses_penggajian_field
from app.services.payroll_service import PayrollService
from app.utils.app_constans import AppConstants
from flask_jwt_extended import get_jwt_identity


payroll_bp = Blueprint('payroll_bp', __name__, url_prefix='/api/payroll')
payroll_api = Api(payroll_bp)

class PayrollController(Resource):

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("pengolahan_gaji")
    def post(self):
        username = get_jwt_identity()

        json = request.get_json()

        schema = PayrollReq()

        validated = schema.load(json)

        response = PayrollService.proses_gaji_grup(username, validated)

        print(response)

        return marshal(response, proses_penggajian_field), 200


payroll_api.add_resource(PayrollController, '')
