from axesdnSDK.ados import create_client
from axesdnSDK.ados.router import GetRouterRangeMonitorRequest
from axesdnSDK.ados.connection import GetConnectionRangeMonitorRequest

import json
from datetime import datetime, timedelta


client = create_client(
    api_access_key="xxxx",
    api_access_secret="xxxx"
)

# range monitor for router
request = GetRouterRangeMonitorRequest(router_uuid="xxx")
request.set_time_range(start=datetime.now()-timedelta(seconds=3600), end=datetime.now())
resp = client.do_request(request)
print(json.dumps(resp, indent=4))

# range monitor for connection
request = GetConnectionRangeMonitorRequest(connection_uuid="xxx")
request.set_time_range(start=datetime.now()-timedelta(seconds=3600), end=datetime.now())
resp = client.do_request(request)
print(json.dumps(resp, indent=4))

