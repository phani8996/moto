from __future__ import unicode_literals

from moto.core.responses import BaseResponse

from .models import athena_backends


class AthenaResponse(BaseResponse):

    @property
    def athena_backend(self):
        return athena_backends[self.region]
