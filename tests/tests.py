#!/usr/bin/env python
import os.path
import random
import string
import unittest

from hostedsms.api import HostedSMSApi
from hostedsms.exceptions import HostedSMSApiException
from hostedsms.responses import *

tests_dir = os.path.abspath(os.path.dirname(__file__))
HSMS_TEST_PHONE = os.environ.get('HSMS_TEST_PHONE', '502505978')
HSMS_TEST_URL = os.environ.get('HSMS_TEST_URL', 'file://' + tests_dir + '/testapi.wsdl')
HSMS_TEST_USERNAME = os.environ.get('HSMS_TEST_USERNAME')
HSMS_TEST_PASSWORD = os.environ.get('HSMS_TEST_PASSWORD')


class BaseHostedSMSApiTest(unittest.TestCase):
    """Base settings"""
    def setUp(self):
        self.phone = HSMS_TEST_PHONE
        self.message = 'Test message'
        self.transaction_id = self.random_transaction_id()
        self.sender = 'INFO'
        self.api = HostedSMSApi(self.username, self.password, url=HSMS_TEST_URL)
        if not all((getattr(self, attr, False) for attr in (
                'username', 'password'))):
            raise unittest.SkipTest('Username and password are required')

    def assertHasAttr(self, obj, attr):
        assert hasattr(obj, attr)

    def randomString(self, size, chars=None):
        if not chars:
            chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(size))

    def random_transaction_id(self, size=20):
        return self.randomString(size=size)

    def random_guid(self):
        return '{}-{}-{}-{}-{}'.format(
            *(self.randomString(size, string.digits) for size in (
                8, 4, 4, 4, 12))
        )


class InvalidCredentialsTest(BaseHostedSMSApiTest):

    def setUp(self):
        """Setup tests"""
        self.username = '1'
        self.password = '1'
        super(InvalidCredentialsTest, self).setUp()

    def test_getdeliveryreports(self):
        """Test if GetDeliveryReports method fails correctly"""
        with self.assertRaises(HostedSMSApiException):
            self.api.get_delivery_reports([self.random_guid()])

    def test_getunreaddeliveryreports(self):
        """Test if GetUnreadDeliveryReports method fails correctly"""
        with self.assertRaises(HostedSMSApiException):
            self.api.get_unread_delivery_reports()

    def test_getvalidsenders(self):
        """Test if GetValidSenders method fails correctly"""
        with self.assertRaises(HostedSMSApiException):
            self.api.get_valid_senders()

    def test_sendsms(self):
        """Test if SendSms method fails correctly"""
        with self.assertRaises(HostedSMSApiException):
            self.api.send_sms(
                self.phone, self.message, self.sender,
                self.transaction_id)

    def test_sendsmses(self):
        """Test if SendSmses method fails correctly"""
        with self.assertRaises(HostedSMSApiException):
            self.api.send_smses(
                [self.phone], self.message, self.sender,
                self.transaction_id)


class CorrectDataTest(BaseHostedSMSApiTest):

    def setUp(self):
        """Setup tests"""
        self.username = HSMS_TEST_USERNAME
        self.password = HSMS_TEST_PASSWORD
        super(CorrectDataTest, self).setUp()

    def assertHasCurrentTime(self, response):
        """Check if response has CurrentTime attribute"""
        self.assertHasAttr(response, 'current_time')

    def test_getdeliveryreports(self):
        """Test if GetDeliveryReports method works correctly"""
        response = self.api.get_delivery_reports([self.random_guid()])
        self.assertIsInstance(response, GetDeliveryReportsResponse)
        self.assertHasCurrentTime(response)
        self.assertIsInstance(response.delivery_reports, list)

    def test_getunreaddeliveryreports(self):
        """Test if GetUnreadDeliveryReports method works correctly"""
        response = self.api.get_unread_delivery_reports()
        self.assertIsInstance(response, GetUnreadDeliveryReportsResponse)
        self.assertHasCurrentTime(response)
        self.assertIsInstance(response.delivery_reports, list)

    def test_getvalidsenders(self):
        """Test if GetValidSenders method works correctly"""
        response = self.api.get_valid_senders()
        self.assertIsInstance(response, GetValidSendersResponse)
        self.assertHasCurrentTime(response)
        self.assertIn(self.sender, response.senders)

    def test_sendsms(self):
        """Test if SendSms method works correctly"""
        response = self.api.send_sms(
            self.phone, self.message, self.sender,
            self.transaction_id)
        self.assertIsInstance(response, SendSmsResponse)
        self.assertHasCurrentTime(response)
        self.assertTrue(response.message_id)

    def test_sendsmses(self):
        """Test if SendSmses method works correctly"""
        response = self.api.send_smses(
            [self.phone], self.message, self.sender,
            self.transaction_id)
        self.assertIsInstance(response, SendSmsesResponse)
        self.assertHasCurrentTime(response)
        self.assertEqual(len(response.message_ids), 1)
        self.assertTrue(response.message_ids[0])

if __name__ == '__main__':
    unittest.main()
