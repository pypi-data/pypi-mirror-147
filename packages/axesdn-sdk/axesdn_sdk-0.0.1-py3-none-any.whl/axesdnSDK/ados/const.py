from enum import Enum


class TopnNum(Enum):
    Top5 = "5"
    Top10 = "10"
    Top15 = "15"
    Top20 = "20"


class TopnSortBy(Enum):
    Flow = "flow"
    Protocol = "protocol"
    Address = "addr"
    Port = "port"


class TopnSortFor(Enum):
    Source = "src"
    Destination = "dst"


class TopnDirection(Enum):
    Uplink = "uplink"
    Downlink = "downlink"


# monitor
DEFAULT_MONITOR_TIME_RANGE_SECONDS = 60
# topn
DEFAULT_TOPN_TIME_RANGE_SECONDS = 900
DEFAULT_TOPN_NUM = TopnNum.Top10
DEFAULT_TOPN_SORT_BY = TopnSortBy.Address
DEFAULT_TOPN_SORT_FOR = TopnSortFor.Source
DEFAULT_TOPN_DIRECTION = TopnDirection.Uplink
# error message
INTERNAL_SERVER_ERROR = "Internal Server Error"
TOKEN_HAS_EXPIRED = "Token has expired"
# client parameter
DEFAULT_CLIENT_ENDPOINT_URL = "https://nest.axesdn.com:8443"
DEFAULT_CLIENT_TIMEOUT_SECONDS = 10
DEFAULT_CLIENT_RETRIES = 5





