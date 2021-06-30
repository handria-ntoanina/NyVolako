from flask import Blueprint, abort, jsonify, current_app, request

from errors import SimpleError
from models import Transaction, Movement, Account, AccountTypeEnum
from utils.auth import requires_auth

bp = Blueprint('transactions', __name__)

# Within a transaction, the sum of the movements amount should equate by following
# this rule: asset + expense + drawing = liability + revenue + equity
LEFT_ACCOUNTS = [AccountTypeEnum.asset, AccountTypeEnum.expense, AccountTypeEnum.drawing]
RIGHT_ACCOUNTS = [AccountTypeEnum.liability, AccountTypeEnum.revenue, AccountTypeEnum.equity]


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
    body = request.get_json()
    db = current_app.db
    try:
        t = Transaction()
        update_transaction_from_body(body, t)
        db.session.add(t)
        db.session.commit()
        return jsonify({
            'success': True
        }), 200
    except Exception as e:
        db.session.rollback()
        raise SimpleError("Cannot post that transaction. {}".format(str(e)), 422)
    finally:
        db.session.close()


@bp.route('/<int:transaction_id>', methods=['PATCH'])
@requires_auth('transactions:update')
def update_transactions(transaction_id):
    t = Transaction.query.get(transaction_id)
    if t is None:
        abort(404)
    db = current_app.db
    body = request.get_json()
    try:
        Movement.query.filter(Movement.transaction == t).delete()
        update_transaction_from_body(body, t)
        db.session.commit()

        return jsonify({
            'success': True
        }), 200
    except Exception as e:
        db.session.rollback()
        raise SimpleError("Cannot post that transaction. {}".format(str(e)), 422)
    finally:
        db.session.close()


@bp.route('/<int:transaction_id>', methods=['DELETE'])
@requires_auth('transactions:delete')
def delete_transactions(transaction_id):
    db = current_app.db
    o = Transaction.query.get(transaction_id)
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
        raise SimpleError("Cannot delete that transaction".format(str(e)), 422)
    finally:
        db.session.close()


def update_transaction_from_body(body, t):
    check_movements_in_body(body)
    t.date = body['date']
    t.description = body['description']
    movements_from_body = body['movements']
    for m in movements_from_body:
        Movement(amount=m['amount'],
                 account=Account.query.get(m['account_id']),
                 transaction=t)


def check_movements_in_body(body):
    if 'movements' not in body:
        raise SimpleError('Cannot find "movements" in the request')
    movements = body['movements']
    if not movements:
        raise SimpleError('"movements" should not be null')
    if len(movements) == 0:
        raise SimpleError('"movements" should not be empty')
    if len([m for m in movements if m['account_id'] is None]) > 0:
        raise SimpleError('Each movement should have an account_id')
    accounts = {m['account_id']: (m['amount'], Account.query.get(m['account_id'])) for m in movements}
    not_found_accounts = [key for key in accounts if accounts[key][1] is None]
    if len(not_found_accounts) > 0:
        raise SimpleError('The following account ids cannot be found {}'.format(', '.join(not_found_accounts)))
    if len([m for m in movements if m['amount'] == 0]) > 0:
        raise SimpleError('There should be no movement with a zero amount')
    left_sum = sum([accounts[key][0] for key in accounts
                    if accounts[key][1] and accounts[key][1].type in LEFT_ACCOUNTS])
    right_sum = sum([accounts[key][0] for key in accounts
                     if accounts[key][1] and accounts[key][1].type in RIGHT_ACCOUNTS])
    if left_sum != right_sum:
        raise SimpleError('The sum of the movements amount does not respect the rule of '
                          '"asset + expense + drawing = liability + revenue + equity"', 422)
