from axesdnSDK.ados.ados_request import AdosRequest
from axesdnSDK.ados.const import *
from axesdnSDK.ados.exception import *
from datetime import datetime, timedelta


class GetRouterSortedTopnRequest(AdosRequest):

    def __init__(self, router_uuid, interfaces):
        """
        Request to get TopN sorted data for router

        :param router_uuid: string, uuid of router
        :param interfaces: [string], list of interface
        """
        super().__init__('get_router_sorted_topn', 'router', 'GET', 'api/v1/router/'+router_uuid+'/topn/sort')
        # set default time range
        self._end_time = datetime.now()
        self._set_param("end", self._end_time.strftime("%Y-%m-%dT%H:%M:%S"))
        self._start_time = self._end_time - timedelta(seconds=DEFAULT_TOPN_TIME_RANGE_SECONDS)
        self._set_param("start", self._start_time.strftime("%Y-%m-%dT%H:%M:%S"))
        # set default parameters for topn
        if not isinstance(interfaces, list):
            raise AdosDataTypeError("parameter 'interfaces' should be a list of string")
        self._ifaces = interfaces
        self._set_param("ifaces", ",".join(self._ifaces))
        self._set_param("top_num", DEFAULT_TOPN_NUM.value)
        self._set_param("sort_for", DEFAULT_TOPN_SORT_FOR.value)
        self._set_param("sort_by", DEFAULT_TOPN_SORT_BY.value)
        self._set_param("direction", DEFAULT_TOPN_DIRECTION.value)

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

    def get_ifaces(self):
        """
        Get list of interface

        :return: [string]
        """
        return self._ifaces

    def set_topn_num(self, top_num):
        """
        Set number of TopN

        :param top_num: TopnNum
        """
        if not isinstance(top_num, TopnNum):
            raise AdosDataTypeError("parameter 'top_num' should be 'TopnNum' type")
        self._set_param("top_num", top_num.value)

    def get_topn_num(self):
        """
        Get number of TopN

        :return: TopnNum
        """
        top_num = self._get_param("top_num")
        return TopnNum(top_num)

    def set_topn_sort_for(self, sort_for):
        """
        Set sort for of TopN

        :param sort_for: TopnSortFor
        """
        if not isinstance(sort_for, TopnSortFor):
            raise AdosDataTypeError("parameter 'sort_for' should be 'TopnSortFor' type")
        self._set_param("sort_for", sort_for.value)

    def get_topn_sort_for(self):
        """
        Get sort for of TopN

        :return: TopnSortFor
        """
        sort_for = self._get_param("sort_for")
        return TopnSortFor(sort_for)

    def set_topn_sort_by(self, sort_by):
        """
        Set sort by of TopN

        :param sort_by: TopnSortBy
        """
        if not isinstance(sort_by, TopnSortBy):
            raise AdosDataTypeError("parameter 'sort_by' should be 'TopnSortBy' type")
        self._set_param("sort_by", sort_by.value)

    def get_topn_sort_by(self):
        """
        Get sort by of TopN

        :return: TopnSortBy
        """
        sort_by = self._get_param("sort_by")
        return TopnSortBy(sort_by)

    def set_topn_direction(self, direction):
        """
        Set direction of TopN

        :param direction: TopnDirection
        """
        if not isinstance(direction, TopnDirection):
            raise AdosDataTypeError("parameter 'direction' should be 'TopnDirection' type")
        self._set_param("direction", direction.value)

    def get_topn_direction(self):
        """
        Get direction of TopN

        :return: TopnDirection
        """
        direction = self._get_param("direction")
        return TopnDirection(direction)
