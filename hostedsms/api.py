from suds.cache import NoCache
from suds.client import Client

from .exceptions import *
from .responses import *
from .settings import HOSTED_SMS_URL


class HostedSMSApi(object):
    """Api for HostedSMS"""

    def __init__(self, username, password, url=None):
        """Set user and password for API

        :param username: User login in hostedsms.pl
        :type username: str
        :param password: User password in hostedsms.pl
        :type password: str

        :param url: option url if differ from specified in settings
        :type url: str

        """
        self.username = username
        self.password = password
        if not url:
            url = HOSTED_SMS_URL
        self._client = Client(url, cache=NoCache())
        self._client.set_options(port='SmsSenderSoap')

    def get_delivery_reports(self, message_ids, mark_as_read=False):
        """Call GetDeliveryReports API method

        :param message_id: List of message ids
        :type message_id: list of str
        :param mark_as_read: Should messages be marked as read
        :type mark_as_read: bool

        :return: Object representing response
        :rtype: GetDeliveryReportsResponse

        :raises HostedSmsApiException: when API return error
        """
        ids_obj = self._client.factory.create('ArrayOfGuid')
        for messageid in message_ids:
            ids_obj.guid.append(messageid)
        response = self._client.service.GetDeliveryReports(
            self.username, self.password, ids_obj, mark_as_read)
        if not response.GetDeliveryReportsResult:
            raise HostedSMSApiException(response.ErrorMessage)
        return GetReadDeliveryReportsResponse(response)

    def get_unread_delivery_reports(self):
        """Call GetUnreadDeliveryReports API method

        :return: Object representing response
        :rtype: GetUnreadDeliveryReportsResponse

        :raises HostedSmsApiException: when API return error
        """
        response = self._client.service.GetUnreadDeliveryReports(
            self.username, self.password)
        if not response.GetUnreadDeliveryReportsResult:
            raise HostedSMSApiException(response.ErrorMessage)
        return GetUnreadDeliveryReportsResponse(response)

    def get_valid_senders(self):
        """Call GetValidSenders API method

        :return: Object representing response
        :rtype: GetValidSendersResponse

        :raises HostedSmsApiException: when API return error
        """
        response = self._client.service.GetValidSenders(
            self.username, self.password)
        if not response.GetValidSendersResult:
            raise HostedSMSApiException(response.ErrorMessage)
        return GetValidSendersResponse(response)

    def send_sms(
            self, phone=None, message=None, sender=None, transaction_id=None,
            validity_period=None, priority=0, flash_sms=False):
        """Call SendSms API method
        :param phone: Phone number where sms should be sent
        :type phone: str
        :param message: Message text
        :type message: str
        :param sender: Sender name (should be in array returned by
            GetValidSenders()
        :type sender: str
        :param transaction_id: Id of transaction
        :type transaction_id: str
        :param validity_period: How long SMS should be valid.
        :type validity_period: datetime
        :param priority: How important is that message
        :type priority: 0..3
        :param flash_sms: Should message be sent as flash sms
        :type flash_sms: bool

        :return: Object representing response
        :rtype: SmsResponse

        :raises HostedSmsApiException: when API return error
        """
        response = self._client.service.SendSms(
            self.username, self.password, phone, message, sender,
            transaction_id, validity_period, priority, flash_sms)
        if not response.SendSmsResult:
            raise HostedSMSApiException(response.ErrorMessage)
        return SendSmsResponse(response)

    def send_smses(
            self, phones, message=None, sender=None,
            transaction_id=None, validity_period=None, priority=0,
            flash_sms=False):
        """Call SendSmses API method
        :param phones: Phone numbers where smses should be sent
        :type phones: list of str
        :param message: Message text
        :type message: str
        :param sender: Sender name (should be in array returned by
            GetValidSenders()
        :type sender: str
        :param transaction_id: Id of transaction
        :type transaction_id: str
        :param validity_period: How long SMS should be valid.
        :type validity_period: datetime
        :param priority: How important is that message
        :type priority: 0..3
        :param flash_sms: Should message be sent as flash sms
        :type flash_sms: bool

        :return: Object representing response
        :rtype: SmsesResponse

        :raises HostedSmsApiException: when API return error
        """
        phones_obj = self._client.factory.create('ArrayOfString')
        for phone in phones:
            phones_obj.string.append(phone)
        response = self._client.service.SendSmses(
            self.username, self.password, phones_obj, message, sender,
            transaction_id, validity_period, priority, flash_sms)
        if not response.SendSmsesResult:
            raise HostedSMSApiException(response.ErrorMessage)
        return SendSmsesResponse(response)
