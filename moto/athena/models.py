from __future__ import unicode_literals

from moto.core import BaseBackend
from uuid import uuid4

from .exceptions import ClientRequestTokenError, InvalidModelError
from .validator import ValidateModel
from ..ec2.models import RegionsAndZonesBackend


class AthenaBackend(BaseBackend):

    def __init__(self, region_name):
        super(AthenaBackend, self).__init__()
        self.region_name = region_name
        self.queries = {}

    def reset(self):
        region_name = self.region_name
        self.__dict__ = {}
        self.__init__(region_name)

    def start_query_execution(self, QueryString, ResultConfiguration, ClientRequestToken = None,
                              QueryExecutionContext=None):
        model_name = 'start_query_execution'
        model = ValidateModel(model_name)
        try:
            model.validate(QueryString, ResultConfiguration, ClientRequestToken, QueryExecutionContext)
        except Exception as ex:
            raise InvalidModelError(model_name, ex)
        if ClientRequestToken is not None and ClientRequestToken in self.queries:
            if self.queries[ClientRequestToken]['query'] != QueryString:
                raise ClientRequestTokenError(ClientRequestToken)
            else:
                return self.queries[ClientRequestToken]['queryExecutionId']
        else:
            if not ClientRequestToken:
                ClientRequestToken = str(uuid4())
            queryExecutionId = str(uuid4())
            self.queries[ClientRequestToken] = {
                'query': QueryString,
                'queryExecutionId': queryExecutionId
            }
            return queryExecutionId


athena_backends = {region.name: AthenaBackend(region.name) for region in RegionsAndZonesBackend.regions}
