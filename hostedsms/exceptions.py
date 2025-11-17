

class HostedSMSException(Exception):
    """Base exception for HostedSMS errors."""
    pass


class HostedSMSApiException(HostedSMSException):
    """Exception for HostedSMS API errors."""
    pass
