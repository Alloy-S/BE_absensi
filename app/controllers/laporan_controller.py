from flask_jwt_extended import get_jwt_identity
from app.filter.jwt_filter import role_required, permission_required
from app.models.pagination_model import PaginationRekapReq, PaginationKuotaCutiReq
from app.models.laporan.laporan_res import rekap_pagination, datang_terlambat_pagination, kuota_cuti_pagination
from app.services.laporan_service import LaporanService
from app.utils.app_constans import AppConstants
from flask_restful import Resource, Api, marshal
from flask import Blueprint, request


laporan_bp = Blueprint('laporan_bp', __name__, url_prefix='/api/laporan')
laporan_api = Api(laporan_bp)

class RekapPeriode(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self):
        query_params = request.args
        schema = PaginationRekapReq()

        validated = schema.load(query_params)

        response = LaporanService.rekap_periode(validated)
        return marshal(response, rekap_pagination), 200

class LaporanDatangTerlambat(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self):
        query_params = request.args
        schema = PaginationRekapReq()

        validated = schema.load(query_params)

        response = LaporanService.laporan_datang_terlambat(validated)

        return marshal(response, datang_terlambat_pagination), 200

class LaporanKuotaCuti(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self):
        query_params = request.args
        schema = PaginationKuotaCutiReq()

        validated = schema.load(query_params)

        response = LaporanService.laporan_kuota_cuti(validated)

        return marshal(response, kuota_cuti_pagination), 200

laporan_api.add_resource(RekapPeriode, '/rekap-periode')
laporan_api.add_resource(LaporanDatangTerlambat, '/datang-terlambat')
laporan_api.add_resource(LaporanKuotaCuti, '/kuota-cuti')