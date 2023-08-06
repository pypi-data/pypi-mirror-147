from axesdnSDK.ados.ados_request import AdosRequest


class GetRoutersInstantMonitorRequest(AdosRequest):

    def __init__(self):
        """
        Request to instant monitor data for all routers
        """
        super().__init__('get_routers_instant_monitor', 'router', 'GET', 'api/v1/routers/monitor/instant')

