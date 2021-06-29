from flask_sqlalchemy import SQLAlchemy
from utils import add_formatter
from .enum import AccountTypeEnum

db = SQLAlchemy()


@add_formatter(parents_to_add=['account'])
class Movement(db.Model):
    __tablename__ = 'movement'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    amount = db.Column(db.Float, nullable=False)
    # This is used to group movements together
    # Within a transaction, the sum of the movements amount should equate by following
    # this rule: asset + expenditure + drawing = liability + revenue + equity
    transaction_id = db.Column(db.Integer, db.ForeignKey('my_transaction.id'))


@add_formatter(children_to_add=['movements'])
class Transaction(db.Model):
    # Using my_transaction as tablename as transaction is a keyword in PostgreSQL
    __tablename__ = 'my_transaction'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    movements = db.relationship('Movement', backref='transaction', foreign_keys=Movement.transaction_id,
                                passive_deletes='all')


@add_formatter(children_to_add=['movements'])
class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    type = db.Column(db.Enum(AccountTypeEnum), nullable=False)
    movements = db.relationship('Movement', backref='account', foreign_keys=Movement.account_id, passive_deletes='all')

    def __repr__(self):
        return (self.type.name + ' - ' if self.type else '') + self.name
