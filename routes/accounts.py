from flask import Blueprint, abort, jsonify, current_app, request
from utils.auth import requires_auth
from models import Account
from models.enum import AccountTypeEnum
from errors import SimpleError

bp = Blueprint('accounts', __name__)


@bp.route('', methods=['GET'])
@requires_auth('accounts:get')
def get_accounts():
    objects = [o.format() for o in Account.query.order_by(Account.type.asc(), Account.name.asc()).all()]
    if len(objects) == 0:
        abort(404)
    return jsonify({
        'success': True,
        'objects': objects
    })


@bp.route('', methods=['POST'])
@requires_auth('accounts:new')
def create():
    db = current_app.db
    body = request.get_json()
    try:
        o = Account()
        o.name = body['name']
        o.type = AccountTypeEnum[body['type']]
        db.session.add(o)
        db.session.commit()
        return jsonify({
            'success': True
        }), 200
    except Exception as e:
        db.session.rollback()
        raise SimpleError("Cannot register that new account".format(str(e)), 422)
    finally:
        db.session.close()


@bp.route('/<int:account_id>', methods=['DELETE'])
@requires_auth('accounts:delete')
def delete(account_id):
    db = current_app.db
    o = Account.query.get(account_id)
    if o is None:
        abort(404)
    try:
        db.session.delete(o)
        db.session.commit()
        return jsonify({
            'success': True
        }), 200
    except Exception as e:
        db.session.rollback()
        raise SimpleError("Cannot delete that account".format(str(e)), 422)
    finally:
        db.session.close()


@bp.route('/<int:account_id>', methods=['PATCH'])
@requires_auth('accounts:update')
def patch(account_id):
    # Should not be able to update type of transaction as it may corrupt the balance of accounts
    db = current_app.db
    o = Account.query.get(account_id)
    if o is None:
        abort(404)
    try:
        body = request.get_json()
        o.name = body['name']
        db.session.commit()
        return jsonify({
            'success': True
        }), 200
    except Exception as e:
        db.session.rollback()
        raise SimpleError("Cannot update that account".format(str(e)), 422)
    finally:
        db.session.close()
