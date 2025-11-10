import unittest
from app import app, db
from models import MFAAccount
import os


class TestSearchEndpoint(unittest.TestCase):
    """Unit tests for the /api/search endpoint"""

    def setUp(self):
        """Set up test client and test database"""
        # Use in-memory database for tests
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.client = app.test_client()

        # Create application context and initialize database
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        # Add test accounts
        test_accounts = [
            MFAAccount(
                account_name='GitHub Account',
                secret='JBSWY3DPEHPK3PXP',
                issuer='GitHub'
            ),
            MFAAccount(
                account_name='Google Account',
                secret='JBSWY3DPEHPK3PXQ',
                issuer='Google'
            ),
            MFAAccount(
                account_name='AWS Console',
                secret='JBSWY3DPEHPK3PXR',
                issuer='Amazon Web Services'
            ),
            MFAAccount(
                account_name='Dropbox',
                secret='JBSWY3DPEHPK3PXS',
                issuer='Dropbox Inc'
            )
        ]

        for account in test_accounts:
            db.session.add(account)
        db.session.commit()

    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_search_returns_all_accounts_when_no_query(self):
        """Test case 1: /api/search returns all accounts when no query is provided"""
        response = self.client.get('/api/search')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(len(data), 4)
        
        # Verify all test accounts are returned
        account_names = {account['account_name'] for account in data}
        self.assertEqual(account_names, {'GitHub Account', 'Google Account', 'AWS Console', 'Dropbox'})

    def test_search_filters_by_account_name(self):
        """Test case 2: /api/search returns filtered accounts when query matches account_name"""
        response = self.client.get('/api/search?q=GitHub')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['account_name'], 'GitHub Account')
        self.assertEqual(data[0]['issuer'], 'GitHub')

    def test_search_filters_by_issuer(self):
        """Test case 3: /api/search returns filtered accounts when query matches issuer"""
        response = self.client.get('/api/search?q=Amazon')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['account_name'], 'AWS Console')
        self.assertEqual(data[0]['issuer'], 'Amazon Web Services')

    def test_search_returns_empty_list_no_matches(self):
        """Test case 4: /api/search returns an empty list if no accounts match the query"""
        response = self.client.get('/api/search?q=NonExistentAccount')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(len(data), 0)
        self.assertEqual(data, [])

    def test_search_response_format(self):
        """Test case 5: /api/search correctly formats the response for each account"""
        response = self.client.get('/api/search?q=Google')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(len(data), 1)

        account = data[0]
        
        # Verify all required fields are present
        self.assertIn('id', account)
        self.assertIn('account_name', account)
        self.assertIn('issuer', account)
        self.assertIn('totp_code', account)
        self.assertIn('remaining_time', account)

        # Verify field types and values
        self.assertIsInstance(account['id'], int)
        self.assertEqual(account['account_name'], 'Google Account')
        self.assertEqual(account['issuer'], 'Google')
        self.assertIsInstance(account['totp_code'], str)
        self.assertEqual(len(account['totp_code']), 6)  # TOTP codes are 6 digits
        self.assertIsInstance(account['remaining_time'], int)
        self.assertGreater(account['remaining_time'], 0)
        self.assertLessEqual(account['remaining_time'], 30)


if __name__ == '__main__':
    unittest.main()
