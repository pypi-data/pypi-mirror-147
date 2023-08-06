from axesdnSDK.ados import create_client
from axesdnSDK.ados.router import GetRouterSortedTopnRequest
from axesdnSDK.ados import TopnNum, TopnDirection, TopnSortBy, TopnSortFor

import json
from datetime import datetime, timedelta


client = create_client(
    api_access_key="xxxx",
    api_access_secret="xxxx"
)

# create request
request = GetRouterSortedTopnRequest(router_uuid="xxx", interfaces=["eth0"])
request.set_time_range(start=datetime.now()-timedelta(seconds=3600), end=datetime.now())
request.set_topn_num(TopnNum.Top20)
request.set_topn_direction(TopnDirection.Downlink)
request.set_topn_sort_by(TopnSortBy.Flow)
request.set_topn_sort_for(TopnSortFor.Destination)

resp = client.do_request(request)
print(json.dumps(resp, indent=4))

