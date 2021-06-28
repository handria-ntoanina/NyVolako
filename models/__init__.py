from flask_sqlalchemy import SQLAlchemy
from utils import add_formatter
from .enum import AccountTypeEnum

db = SQLAlchemy()


@add_formatter()
class Movement(db.Model):
    __tablename__ = 'movement'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    # This is used to group movements together
    # Within a transaction, the sum of the movements amount should equate by following
    # this rule: asset + expenditure + drawing = liability + revenue + equity
    transaction_id = db.Column(db.String, nullable=False)


@add_formatter()
class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    type = db.Column(db.Enum(AccountTypeEnum))
    movements = db.relationsip('Movement', backref='account', foreign_keys=Movement.account_id)
