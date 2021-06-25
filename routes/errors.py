from flask import Blueprint, jsonify, current_app
from sqlalchemy.exc import IntegrityError
from errors import AuthError, SimpleError
import traceback
from utils import has_text

bp = Blueprint('errors', __name__)


@bp.app_errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


@bp.app_errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden"
    }), 403


@bp.app_errorhandler(401)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401


@bp.app_errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "No matching resources was found"
    }), 404


@bp.app_errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@bp.app_errorhandler(IntegrityError)
def integrity_error(error):
    return jsonify({
        "success": False,
        "error": 409,
        "message": str(error)
    }), 409


@bp.app_errorhandler(SimpleError)
def simple_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.message
    }), error.status_code


@bp.app_errorhandler(ValueError)
def value_error(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": str(error)
    }), 400


@bp.app_errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code


def default_handler(error):
    message = str(error) + '\n' if has_text(str(error)) else ''
    message += traceback.format_exc() if current_app.config['TRACE_MODE'] else ''
    print(traceback.format_exc())
    return jsonify({
        "success": False,
        "error": 500,
        "message": message
    }), 500
