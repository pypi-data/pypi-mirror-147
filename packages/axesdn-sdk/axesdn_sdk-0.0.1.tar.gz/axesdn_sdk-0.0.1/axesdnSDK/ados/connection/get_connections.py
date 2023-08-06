from axesdnSDK.ados.ados_request import AdosRequest


class GetConnectionsRequest(AdosRequest):

    def __init__(self):
        """
        Request to get all connections
        """
        super().__init__('get_connections', 'connection', 'GET', 'api/v1/connections')

