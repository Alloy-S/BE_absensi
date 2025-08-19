from app.models.pagination_model import PaginationRiwayatPenggajianReq
from app.models.payroll.payroll_req import PayrollReq
from flask import request, Blueprint
from flask_restful import Resource, Api, marshal
from app.filter.jwt_filter import role_required, permission_required
from app.models.payroll.payroll_res import rincian_perhitung_field, hasil_penggajian_field, proses_penggajian_field
from app.models.riwayat_penggajian.riwayat_penggajian_res import riwayat_penggajian_field, \
    riwayat_penggajian_pagination, export_excel_field
from app.services.payroll_service import PayrollService
from app.utils.app_constans import AppConstants
from flask_jwt_extended import get_jwt_identity


riwayat_penggajian_bp = Blueprint('riwayat_penggajian_bp', __name__, url_prefix='/api/riwayat-penggajian')
riwayat_penggajian_api = Api(riwayat_penggajian_bp)

class FinalisasiRiwayatPenggajianController(Resource):

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("pengolahan_gaji")
    def post(self, riwayat_id):

        PayrollService.finalisasi_riwayat_penggajian(riwayat_id)

        return None, 200

class RiwayatPenggajianByIdController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("pengolahan_gaji")
    def get(self, riwayat_id):
        response = PayrollService.get_riwayat_by_id(riwayat_id)

        return marshal(response, riwayat_penggajian_field), 200


class RiwayatPenggajianController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("pengolahan_gaji")
    def get(self):
        params = request.args

        schema = PaginationRiwayatPenggajianReq()

        validated = schema.load(params)
        response = PayrollService.get_riwayat_penggajian_pagination(validated)

        response = {
            'pages': response.pages,
            'total': response.total,
            'items': response.items,
        }

        return marshal(response, riwayat_penggajian_pagination), 200

class ExportRiwayatPenggajianByIdController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("pengolahan_gaji")
    def get(self, riwayat_id):
        response = PayrollService.export_riwayat_penggajian_to_excel(riwayat_id)

        return marshal(response, export_excel_field), 200


riwayat_penggajian_api.add_resource(FinalisasiRiwayatPenggajianController, '/<string:riwayat_id>/finalisasi')
riwayat_penggajian_api.add_resource(RiwayatPenggajianByIdController, '/<string:riwayat_id>')
riwayat_penggajian_api.add_resource(RiwayatPenggajianController, '')
riwayat_penggajian_api.add_resource(ExportRiwayatPenggajianByIdController, '/<string:riwayat_id>/export')
