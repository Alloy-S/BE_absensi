from flask import Blueprint, jsonify
from marshmallow import ValidationError
from flask import jsonify, current_app
from app.database import db
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
    response.status_code = error.status_code
    return response


@errors_bp.app_errorhandler(ValidationError)
def validation_error_handler(error):
    response_data = {
        "message": error.messages
    }
    response = jsonify(response_data)
    response.status_code = 400
    return response


@errors_bp.app_errorhandler(Exception)
def handle_internal_error(error):
    current_app.logger.error(f"Unhandled Exception: {error}", exc_info=True)

    try:
        db.session.rollback()
    except Exception as e:
        current_app.logger.error(f"Failed to rollback database session: {e}")

    response_data = {
        "message": 'Internal Server Error'
    }
    response = jsonify(response_data)
    response.status_code = 500
    return response


@errors_bp.app_errorhandler(404)
def handle_not_found_error(error):
    response_data = {
        "message": "Resource yang Anda tuju tidak dapat ditemukan di server."
    }
    response = jsonify(response_data)
    response.status_code = 404
    return response
