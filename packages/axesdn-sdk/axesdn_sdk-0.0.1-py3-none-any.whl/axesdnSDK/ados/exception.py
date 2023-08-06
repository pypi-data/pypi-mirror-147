from axesdnSDK.exception import AxesdnError


class AdosError(AxesdnError):
    """ADOS Error."""


class AdosParameterError(AdosError):
    """Parameter Error"""


class AdosParseError(AdosError):
    """Parse Error"""


class AdosDataTypeError(AdosError):
    """Data Type Error"""


class AdosServerError(AdosError):
    """Server Error."""


class AdosClientError(AdosError):
    """Client Error."""


class AdosLoginError(AdosError):
    """Login Error."""


class AdosRefreshError(AdosError):
    """Refresh Error."""

