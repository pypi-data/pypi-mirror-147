from axesdnSDK.ados.ados_request import AdosRequest


class GetConnectionsInstantMonitorRequest(AdosRequest):

    def __init__(self):
        """
        Request to instant monitor data for all connections
        """
        super().__init__('get_connections_instant_monitor', 'connection', 'GET', 'api/v1/connections/monitor/instant')

