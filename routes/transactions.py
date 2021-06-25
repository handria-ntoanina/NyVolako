from flask import Blueprint, abort, jsonify
from utils.auth import requires_auth
from models import Movement

bp = Blueprint('transactions', __name__)


@bp.route('', methods=['GET'])
@requires_auth('transactions:get')
def get_transactions():
    objects = [o.format() for o in Movement.query.order_by(Movement.date.asc(), Movement.transaction_id.asc()).all]
    if len(objects) == 0:
        abort(404)
    return jsonify({
        'success': True,
        'objects': objects
    })