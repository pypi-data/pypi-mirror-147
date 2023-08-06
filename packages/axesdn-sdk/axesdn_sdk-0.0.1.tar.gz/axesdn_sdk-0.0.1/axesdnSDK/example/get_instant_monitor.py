from axesdnSDK.ados import create_client
from axesdnSDK.ados.router import GetRoutersInstantMonitorRequest
from axesdnSDK.ados.connection import GetConnectionsInstantMonitorRequest

import json


client = create_client(
    api_access_key="xxxx",
    api_access_secret="xxxx"
)

# instant monitor for routers
request = GetRoutersInstantMonitorRequest()
resp = client.do_request(request)
print(json.dumps(resp, indent=4))

# instant monitor for connections
request = GetConnectionsInstantMonitorRequest()
resp = client.do_request(request)
print(json.dumps(resp, indent=4))

