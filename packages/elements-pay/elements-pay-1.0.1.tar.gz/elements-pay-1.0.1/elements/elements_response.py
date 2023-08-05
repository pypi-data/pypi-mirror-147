from __future__ import absolute_import

import json


class ElementsResponse(object):
    def __init__(self, status, body, headers):
        self.status = status
        self.headers = headers
        self.body = body
        self.data = json.loads(body)
