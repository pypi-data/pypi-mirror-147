from axesdnSDK.ados.ados_request import AdosRequest
from axesdnSDK.ados.const import *
from axesdnSDK.ados.exception import *
from datetime import datetime, timedelta


class GetConnectionRangeMonitorRequest(AdosRequest):

    def __init__(self, connection_uuid):
        """
        Request to get monitor data with range for connection

        :param connection_uuid: string, uuid of connection
        """
        super().__init__('get_connection_range_monitor', 'connection', 'GET', 'api/v1/connection/'+connection_uuid+'/monitor/range')
        # set default time range
        self._end_time = datetime.now()
        self._set_param("end", self._end_time.strftime("%Y-%m-%dT%H:%M:%S"))
        self._start_time = self._end_time - timedelta(seconds=DEFAULT_MONITOR_TIME_RANGE_SECONDS)
        self._set_param("start", self._start_time.strftime("%Y-%m-%dT%H:%M:%S"))

    def set_time_range(self, start, end):
        """
        Set time range for request

        :param start: datetime, start time of request
        :param end: datetime, end time of request
        """

        if not isinstance(start, datetime):
            raise AdosDataTypeError("parameter 'start' is not datetime type")
        if not isinstance(end, datetime):
            raise AdosDataTypeError("parameter 'end' is not datetime type")
        if (end - start).total_seconds() <= 0:
            raise AdosParameterError("parameter 'end' can't be less equal than 'start'")
        self._end_time = end
        self._set_param("end", end.strftime("%Y-%m-%dT%H:%M:%S"))
        self._start_time = start
        self._set_param("start", start.strftime("%Y-%m-%dT%H:%M:%S"))

    def get_start_time(self):
        """
        Get start time of time range

        :return: datetime
        """

        return self._start_time

    def get_end_time(self):
        """
        Get end time of time range

        :return: datetime
        """
        return self._end_time

