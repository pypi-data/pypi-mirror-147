from axesdnSDK.ados.ados_request import AdosRequest


class GetRoutersRequest(AdosRequest):

    def __init__(self):
        """
        Request to get all routers
        """
        super().__init__('get_routers', 'router', 'GET', 'api/v1/routers')

