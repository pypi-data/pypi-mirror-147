from . import sim_template_pb2_grpc as importStub

class SimTemplateService(object):

    def __init__(self, router):
        self.connector = router.get_connection(SimTemplateService, importStub.SimTemplateStub)

    def createNOSRule(self, request, timeout=None):
        return self.connector.create_request('createNOSRule', request, timeout)

    def createAmendRule(self, request, timeout=None):
        return self.connector.create_request('createAmendRule', request, timeout)

    def createCancelRule(self, request, timeout=None):
        return self.connector.create_request('createCancelRule', request, timeout)

    def createQuoteRule(self, request, timeout=None):
        return self.connector.create_request('createQuoteRule', request, timeout)

    def createSecurityRule(self, request, timeout=None):
        return self.connector.create_request('createSecurityRule', request, timeout)