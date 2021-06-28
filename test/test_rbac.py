import unittest

from test import DefaultTestCase


class RbacTestCase(DefaultTestCase):
    """
    Accountant:
        Manages accounts,
        post new transactions, update transactions, delete transactions, get transactions
    Secretary:
        Post new transactions
        View accounts
        View transactions
    """
    def test_accountant_add_account(self):
        pass

    def test_accountant_update_account(self):
        pass

    def test_accountant_delete_account(self):
        pass

    def test_accountant_get_accounts(self):
        pass

    def test_accountant_post_new_transaction(self):
        pass

    def test_accountant_update_transaction(self):
        pass

    def test_accountant_delete_transaction(self):
        pass

    def test_accountant_get_transactions(self):
        pass

    def test_secretary_forbidden_actions(self):
        pass

    def test_secretary_post_transactions(self):
        pass

    def test_secretary_get_accounts(self):
        pass

    def test_secretary_get_transactions(self):
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
