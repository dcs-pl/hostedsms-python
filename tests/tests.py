#!/usr/bin/env python
import os
import random
import string
import unittest
import uuid
from datetime import datetime, timedelta
from typing import Any, Optional
from hostedsms.api import HostedSMSApi
from hostedsms.exceptions import HostedSMSApiException
from hostedsms.responses import (
    GetDeliveryReportsResponse, GetUnreadDeliveryReportsResponse, GetValidSendersResponse,
    SendSmsResponse, SendSmsesResponse, GetInputSmsesResponse
)

tests_dir = os.path.abspath(os.path.dirname(__file__))
HSMS_TEST_PHONE: str = os.environ.get('HSMS_TEST_PHONE', '502505978')
HSMS_TEST_URL: str = os.environ.get('HSMS_TEST_URL', 'file://' + os.path.join(tests_dir, 'testapi.wsdl'))
HSMS_TEST_USERNAME: str = os.environ.get('HSMS_TEST_USERNAME', '')
HSMS_TEST_PASSWORD: str = os.environ.get('HSMS_TEST_PASSWORD', '')


class BaseHostedSMSApiTest(unittest.TestCase):
    """Base settings for HostedSMS API tests."""
 
    username: str = ''
    password: str = ''

    def setUp(self) -> None:
        self.phone: str = HSMS_TEST_PHONE
        self.message: str = 'Test message'
        self.transaction_id: str = self.random_transaction_id()
        self.sender: str = 'INFO'
        print(HSMS_TEST_URL)
        self.api: HostedSMSApi = HostedSMSApi(self.username, self.password, url=HSMS_TEST_URL)
        if not all((getattr(self, attr, False) for attr in ('username', 'password'))):
            raise unittest.SkipTest('Username and password are required')

    def assertHasAttr(self, obj: Any, attr: str) -> None:
        assert hasattr(obj, attr)

    def randomString(self, size: int, chars: Optional[str] = None) -> str:
        if not chars:
            chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(size))

    def random_transaction_id(self, size: int = 20) -> str:
        return self.randomString(size=size)

    def random_guid(self) -> str:
        return str(uuid.uuid4())


class InvalidCredentialsTest(BaseHostedSMSApiTest):
    """Test HostedSMS API with invalid credentials."""
    def setUp(self) -> None:
        self.username: str = '1'
        self.password: str = '1'
        super().setUp()

    def test_getdeliveryreports(self) -> None:
        
        with self.assertRaises(HostedSMSApiException):
            self.api.get_delivery_reports([self.random_guid()])

    def test_getunreaddeliveryreports(self) -> None:
        with self.assertRaises(HostedSMSApiException):
            self.api.get_unread_delivery_reports()

    def test_getvalidsenders(self) -> None:
        with self.assertRaises(HostedSMSApiException):
            self.api.get_valid_senders()

    def test_sendsms(self) -> None:
        with self.assertRaises(HostedSMSApiException):
            self.api.send_sms(self.phone, self.message, self.sender, self.transaction_id)

    def test_sendsmses(self) -> None:
        with self.assertRaises(HostedSMSApiException):
            self.api.send_smses([self.phone], self.message, self.sender, self.transaction_id)

    def test_getinputsmses(self) -> None:
        with self.assertRaises(HostedSMSApiException):
            self.api.get_input_smses(datetime.now() - timedelta(weeks=1), datetime.now(), self.phone, True)

    def test_getunreadinputsmses(self) -> None:
        with self.assertRaises(HostedSMSApiException):
            self.api.get_unread_input_smses()


class CorrectDataTest(BaseHostedSMSApiTest):
    """Test HostedSMS API with correct credentials."""
    def setUp(self) -> None:
        self.username: str = HSMS_TEST_USERNAME
        self.password: str = HSMS_TEST_PASSWORD
        super().setUp()

    def assertHasCurrentTime(self, response: Any) -> None:
        self.assertHasAttr(response, 'current_time')

    def test_getdeliveryreports(self) -> None:
        response = self.api.get_delivery_reports([self.random_guid()])
        self.assertIsInstance(response, GetDeliveryReportsResponse)
        self.assertHasCurrentTime(response)
        self.assertIsInstance(response.delivery_reports, list)

    def test_getunreaddeliveryreports(self) -> None:
        response = self.api.get_unread_delivery_reports()
        self.assertIsInstance(response, GetUnreadDeliveryReportsResponse)
        self.assertHasCurrentTime(response)
        self.assertIsInstance(response.delivery_reports, list)

    def test_getvalidsenders(self) -> None:
        response = self.api.get_valid_senders()
        self.assertIsInstance(response, GetValidSendersResponse)
        self.assertHasCurrentTime(response)
        self.assertIn(self.sender, response.senders)

    def test_sendsms(self) -> None:
        response = self.api.send_sms(self.phone, self.message, self.sender, self.transaction_id)
        self.assertIsInstance(response, SendSmsResponse)
        self.assertHasCurrentTime(response)
        self.assertTrue(response.message_id)

    def test_sendsmses(self) -> None:
        response = self.api.send_smses([self.phone], self.message, self.sender, self.transaction_id)
        self.assertIsInstance(response, SendSmsesResponse)
        self.assertHasCurrentTime(response)
        self.assertEqual(len(response.message_ids), 1)
        self.assertTrue(response.message_ids[0])

    def test_getinputsmses(self) -> None:
        response = self.api.get_input_smses(datetime.now() - timedelta(weeks=600), datetime.now(), self.phone, False)
        self.assertIsInstance(response, GetInputSmsesResponse)
        self.assertHasCurrentTime(response)
        self.assertIsInstance(response.input_sms, list)

    def test_getunreadinputsmses(self) -> None:
        response = self.api.get_unread_input_smses()
        self.assertIsInstance(response, GetInputSmsesResponse)
        self.assertHasCurrentTime(response)
        self.assertIsInstance(response.input_sms, list)


if __name__ == '__main__':
    unittest.main()
