from axesdnSDK.ados import create_client
from axesdnSDK.ados.router import GetRoutersRequest
from axesdnSDK.ados.connection import GetConnectionsRequest

import json


client = create_client(
    api_access_key="xxxx",
    api_access_secret="xxxx"
)

# get routers
request = GetRoutersRequest()
resp = client.do_request(request)
print(json.dumps(resp, indent=4))

# get connections
request = GetConnectionsRequest()
resp = client.do_request(request)
print(json.dumps(resp, indent=4))
