from flask import Blueprint, jsonify
from app.execption.custom_execption import GeneralExceptionWithParam, GeneralException

errors_bp = Blueprint('execption_handler', __name__)

@errors_bp.app_errorhandler(GeneralExceptionWithParam)
def handle_general_exception_with_param(error):
    response_data = {
        "message": error.message
    }
    response = jsonify(response_data)
    response.status_code = error.status_code
    return response

@errors_bp.app_errorhandler(GeneralException)
def handle_general_exception(error):
    response_data = {
        "message": error.message
    }
    response = jsonify(response_data)
    response.status_code = 400
    return response

@errors_bp.app_errorhandler(Exception)
def handle_internal_error():
    response_data = {
        "message": 'Internal Server Error'
    }
    response = jsonify(response_data)
    response.status_code = 500
    return response