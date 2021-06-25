from flask_sqlalchemy import SQLAlchemy
from utils import add_formatter
from .enum import AccountTypeEnum

db = SQLAlchemy()


@add_formatter()
class Movement(db.Model):
    __tablename__ = 'movement'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    amount = db.Column(db.Float)
    # This is used to group movements together
    # the sum of
    transaction_id = db.Column(db.String)


@add_formatter()
class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    type = db.Column(db.Enum(AccountTypeEnum))
    movements = db.relationsip('Movement', backref='account', foreign_keys=Movement.account_id)
