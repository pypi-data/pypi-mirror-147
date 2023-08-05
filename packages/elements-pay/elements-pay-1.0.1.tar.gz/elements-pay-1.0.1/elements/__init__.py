from __future__ import absolute_import, print_function

import os

API_PRODUCTION = "https://api.elements.io"
API_SANDBOX = "https://api.elements-sandbox.io"

api_base = API_PRODUCTION
api_key = None
logger = None

max_network_retries = 0
min_network_retry_delay = 0.5
max_network_retry_delay = 2.0

ssl_verify_certs = True
ssl_ca_file = os.path.join(os.path.dirname(__file__), "certs", "cacert.pem")

with open(os.path.join(os.path.dirname(__file__), "..", "VERSION")) as f:
    version = f.read()

from elements.resources import *
