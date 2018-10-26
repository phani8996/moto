from __future__ import unicode_literals
from .responses import AthenaResponse

url_bases = [
    "https?://autoscaling.(.+).amazonaws.com",
]

url_paths = {
    '{0}/$': AthenaResponse.dispatch,
}
