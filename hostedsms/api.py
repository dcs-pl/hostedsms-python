from datetime import datetime
from typing import Any, List, Optional
from suds.cache import NoCache
from suds.client import Client
from .exceptions import HostedSMSApiException
from .responses import (
    GetUnreadDeliveryReportsResponse, GetReadDeliveryReportsResponse,
    GetValidSendersResponse, SendSmsResponse, SendSmsesResponse, GetInputSmsesResponse
)
from .settings import HOSTED_SMS_URL


class HostedSMSApi:
    """Api for HostedSMS"""
    def __init__(self, username: str, password: str, url: Optional[str] = None):
        self.username: str = username
        self.password: str = password
        if not url:
            url = HOSTED_SMS_URL
        self._client: Client = Client(url, cache=NoCache())
        self._client.set_options(port='SmsSenderSoap')

    def get_delivery_reports(self, message_ids: List[str], mark_as_read: bool = False) -> GetReadDeliveryReportsResponse:
        """Get delivery reports for given message IDs."""
        ids_obj = self._client.factory.create('ArrayOfGuid')
        for messageid in message_ids:
            ids_obj.guid.append(messageid)
        response = self._client.service.GetDeliveryReports(
            self.username, self.password, ids_obj, mark_as_read)
        if not response.GetDeliveryReportsResult:
            raise HostedSMSApiException(response.ErrorMessage)
        return GetReadDeliveryReportsResponse(response)

    def get_unread_delivery_reports(self) -> GetUnreadDeliveryReportsResponse:
        """Get unread delivery reports."""
        response = self._client.service.GetUnreadDeliveryReports(
            self.username, self.password)
        if not response.GetUnreadDeliveryReportsResult:
            raise HostedSMSApiException(response.ErrorMessage)
        return GetUnreadDeliveryReportsResponse(response)

    def get_valid_senders(self) -> GetValidSendersResponse:
        """Get valid senders for the account."""
        response = self._client.service.GetValidSenders(
            self.username, self.password)
        if not response.GetValidSendersResult:
            raise HostedSMSApiException(response.ErrorMessage)
        return GetValidSendersResponse(response)

    def send_sms(
        self, phone: Optional[str] = None, message: Optional[str] = None, sender: Optional[str] = None, transaction_id: Optional[str] = None,
        validity_period: Any = None, priority: int = 0, flash_sms: bool = False
    ) -> SendSmsResponse:
        """Send a single SMS message."""
        response = self._client.service.SendSms(
            self.username, self.password, phone, message, sender,
            transaction_id, validity_period, priority, flash_sms)
        if not response.SendSmsResult:
            raise HostedSMSApiException(response.ErrorMessage)
        return SendSmsResponse(response)

    def send_smses(
        self, phones: List[str], message: Optional[str] = None, sender: Optional[str] = None,
        transaction_id: Optional[str] = None, validity_period: Any = None, priority: int = 0,
        flash_sms: bool = False
    ) -> SendSmsesResponse:
        """Send multiple SMS messages."""
        phones_obj = self._client.factory.create('ArrayOfString')
        for phone in phones:
            phones_obj.string.append(phone)
        response = self._client.service.SendSmses(
            self.username, self.password, phones_obj, message, sender,
            transaction_id, validity_period, priority, flash_sms)
        if not response.SendSmsesResult:
            raise HostedSMSApiException(response.ErrorMessage)
        return SendSmsesResponse(response)

    def get_input_smses(self, _from: Optional[datetime]=None, to: Optional[datetime]=None, receipient: Optional[str]=None, mark_as_read: bool=False) -> GetInputSmsesResponse:
        """Get input SMS messages for a given period and recipient."""
        response = self._client.service.GetInputSmses(
            self.username, self.password, _from, to, receipient, mark_as_read)
        if not response.GetInputSmsesResult:
            raise HostedSMSApiException(response.ErrorMessage)
        return GetInputSmsesResponse(response)

    def get_unread_input_smses(self) -> GetInputSmsesResponse:
        """Get unread input SMS messages."""
        response = self._client.service.GetUnreadInputSmses(
            self.username, self.password)
        if not response.GetUnreadInputSmsesResult:
            raise HostedSMSApiException(response.ErrorMessage)
        return GetInputSmsesResponse(response)