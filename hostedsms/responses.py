"""
See WebApi documentation https://api.hostedsms.pl/WS/smssender.asmx
"""


class HostedSmsApiResponse(object):
    """Base class for all respones"""
    def __init__(self, response):
        self.current_time = response.CurrentTime


class DeliveryReport(object):

    def __init__(self, report):
        self.report_id = str(report.ReportId)
        self.phone = str(report.Phone)
        self.message_id = str(report.MessageId)
        self.status = int(report.Status)
        self.delivery_time = report.DeliveryTime

    def __repr__(self):
        return '<DeliveryReport {0}>'.format(self.report_id)


class GetDeliveryReportsResponse(HostedSmsApiResponse):

    def __init__(self, response):
        super(GetDeliveryReportsResponse, self).__init__(response)
        self.delivery_reports = []
        if response.DeliveryReports:
            reports = response.DeliveryReports.DeliveryReport
            for report in reports:
                self.delivery_reports.append(DeliveryReport(report))

    def __repr__(self):
        return '<GetUnreadDeliveryReports {0}>'.format(self.current_time)


class GetUnreadDeliveryReportsResponse(GetDeliveryReportsResponse):
    pass


class GetReadDeliveryReportsResponse(GetDeliveryReportsResponse):
    pass


class GetValidSendersResponse(HostedSmsApiResponse):

    def __init__(self, response):
        super(GetValidSendersResponse, self).__init__(response)
        self.senders = []
        for sender in response.Senders.string:
            self.senders.append(str(sender))


class SendSmsResponse(HostedSmsApiResponse):

    def __init__(self, response):
        super(SendSmsResponse, self).__init__(response)
        self.message_id = str(response.MessageId)


class SendSmsesResponse(HostedSmsApiResponse):

    def __init__(self, response):
        super(SendSmsesResponse, self).__init__(response)
        self.message_ids = []
        for msg_id in response.MessageIds.guid:
            self.message_ids.append(str(msg_id))
