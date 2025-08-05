from flask_jwt_extended import get_jwt_identity
from app.filter.jwt_filter import role_required, permission_required
from app.models.pagination_model import PaginationReq, PaginationRekapReq
from app.models.rekap_periode.rekap_periode_res import rekap_periode_field, rekap_pagination
from app.services.rekap_periode_service import RekapPeriodeService
from app.utils.app_constans import AppConstants
from flask_restful import Resource, Api, marshal
from flask import Blueprint, request


rekap_periode_bp = Blueprint('rekap_periode_bp', __name__, url_prefix='/api/rekap-periode')
rekap_periode_api = Api(rekap_periode_bp)

class RekapPeriode(Resource):
    def get(self):
        queryparams = request.args
        schema = PaginationRekapReq()

        validated = schema.load(queryparams)

        response = RekapPeriodeService.rekap_periode(validated)
        return marshal(response, rekap_pagination), 200


rekap_periode_api.add_resource(RekapPeriode, '')