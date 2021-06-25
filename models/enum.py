import enum


class AccountTypeEnum(enum.Enum):
    asset = 'asset'
    expense = 'expense'
    drawing = 'drawing'
    liability = 'liability'
    revenue = 'revenue'
    equity = 'equity'

