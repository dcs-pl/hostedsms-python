"""
See WebApi documentation https://api.hostedsms.pl/WS/smssender.asmx
"""


from datetime import datetime
from typing import Any, List, Optional
from dataclasses import dataclass

__all__ = [
    "HostedSmsApiResponse", "DeliveryReport", "GetDeliveryReportsResponse",
    "GetUnreadDeliveryReportsResponse", "GetReadDeliveryReportsResponse",
    "GetValidSendersResponse", "SendSmsResponse", "SendSmsesResponse",
    "GetInputSmsesResponse", "InputSms"
]


class HostedSmsApiResponse:
    """Base class for all API responses."""
    def __init__(self, response: Any):
        self.current_time: Any = getattr(response, 'CurrentTime', None)


@dataclass
class DeliveryReport:
    report_id: str
    phone: str
    message_id: str
    status: int
    delivery_time: datetime

    def __init__(self, report: Any):
        self.report_id = str(getattr(report, 'ReportId', ''))
        self.phone = str(getattr(report, 'Phone', ''))
        self.message_id = str(getattr(report, 'MessageId', ''))
        self.status = int(getattr(report, 'Status', 0))
        self.delivery_time = getattr(report, 'DeliveryTime')


class GetDeliveryReportsResponse(HostedSmsApiResponse):
    """Response for delivery reports."""
    def __init__(self, response: Any):
        super().__init__(response)
        self.delivery_reports: List[DeliveryReport] = [
            DeliveryReport(report) for report in getattr(getattr(response, 'DeliveryReports', None), 'DeliveryReport', [])
        ]


class GetUnreadDeliveryReportsResponse(GetDeliveryReportsResponse):
    """Response for unread delivery reports."""
    pass


class GetReadDeliveryReportsResponse(GetDeliveryReportsResponse):
    """Response for read delivery reports."""
    pass


class GetValidSendersResponse(HostedSmsApiResponse):
    """Response for valid senders."""
    def __init__(self, response: Any):
        super().__init__(response)
        self.senders: List[str] = [str(sender) for sender in getattr(getattr(response, 'Senders', None), 'string', [])]


class SendSmsResponse(HostedSmsApiResponse):
    """Response for sending a single SMS."""
    def __init__(self, response: Any):
        super().__init__(response)
        self.message_id: str = str(getattr(response, 'MessageId', ''))


class SendSmsesResponse(HostedSmsApiResponse):
    """Response for sending multiple SMS messages."""
    def __init__(self, response: Any):
        super().__init__(response)
        self.message_ids: List[str] = [str(msg_id) for msg_id in getattr(getattr(response, 'MessageIds', None), 'guid', [])]


class GetInputSmsesResponse(HostedSmsApiResponse):
    """Response for input SMS messages."""
    def __init__(self, response: Any):
        super().__init__(response)
        self._raw_response = response
        self.input_sms: List[InputSms] = [InputSms(sms) for sms in getattr(getattr(response, 'InputSms', []), 'InputSms', [])]


@dataclass
class InputSms:
    message_id: str
    phone: str
    recipient: str
    message: str
    received_time: Optional[datetime]

    def __init__(self, sms: Any):
        self.message_id = str(getattr(sms, 'MessageId', ''))
        self.phone = str(getattr(sms, 'Phone', ''))
        self.recipient = str(getattr(sms, 'Recipient', ''))
        self.message = str(getattr(sms, 'Message', ''))
        received_time = getattr(sms, 'ReceivedTime', None)
        if received_time is None:
            self.received_time = received_time
        else:
            try:
                self.received_time = datetime.fromisoformat(str(received_time))
            except Exception:
                self.received_time = None
