from flask import Blueprint, abort, jsonify

from models import Transaction
from utils.auth import requires_auth

bp = Blueprint('transactions', __name__)


@bp.route('', methods=['GET'])
@requires_auth('transactions:get')
def get_transactions():
    objects = [o.format() for o in Transaction.query.order_by(Transaction.date.asc()).all()]
    if len(objects) == 0:
        abort(404)
    return jsonify({
        'success': True,
        'objects': objects
    })


@bp.route('', methods=['POST'])
@requires_auth('transactions:new')
def post_transactions():
    pass


@bp.route('/<int:transaction_id>', methods=['PATCH'])
@requires_auth('transactions:update')
def update_transactions(transaction_id):
    pass


@bp.route('/<int:transaction_id>', methods=['DELETE'])
@requires_auth('transactions:delete')
def delete_transactions(transaction_id):
    pass
