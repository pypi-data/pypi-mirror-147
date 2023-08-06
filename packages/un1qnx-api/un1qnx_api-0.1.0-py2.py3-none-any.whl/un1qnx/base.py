#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from . import tag
from . import product

UN1QNX_BASE_URL = "https://un1qone-backend-test.azurewebsites.net/api/v2/"
""" The default base URL to be used when no other
base URL value is provided to the constructor """

UN1QNX_AUTH_URL = "https://un1qone-identity-server-test.azurewebsites.net/"
""" The default auth URL to be used when no other
auth URL value is provided to the constructor """

class API(
    appier.API,
    tag.TagAPI,
    product.ProductAPI
):

    def __init__(self, *args, **kwargs):
        appier.API.__init__(self, *args, **kwargs)
        self.base_url = appier.conf("UN1QNX_BASE_URL", UN1QNX_BASE_URL)
        self.auth_url = appier.conf("UN1QNX_AUTH_URL", UN1QNX_AUTH_URL)
        self.base_url = kwargs.get("base_url", self.base_url)
        self.auth_url = kwargs.get("auth_url", self.auth_url)
        self.token = kwargs.get("token", None)
        self.client_id = kwargs.get("client_id", None)
        self.client_secret = kwargs.get("client_secret", None)
        self.grant_type = kwargs.get("grant_type", "client_credentials")

    def build(
        self,
        method,
        url,
        data = None,
        data_j = None,
        data_m = None,
        headers = None,
        params = None,
        mime = None,
        kwargs = None
    ):
        auth = kwargs.pop("auth", True)
        if auth: headers["Authorization"] = self.auth_header()

    def get_token(self):
        if self.token: return self.token

        url = self.auth_url + "connect/token"
        params = dict(
            client_id = self.client_id,
            client_secret = self.client_secret,
            grant_type = self.grant_type
        )
        contents = self.post(url, params = params, auth = False)

        self.token = contents.get("access_token", None)
        return self.token

    def auth_callback(self, params, headers):
        self.token = None
        headers["Authorization"] = self.auth_header()

    def auth_header(self):
        return "Bearer %s" % self.get_token()
