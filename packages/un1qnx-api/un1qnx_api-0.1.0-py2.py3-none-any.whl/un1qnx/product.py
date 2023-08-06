#!/usr/bin/python
# -*- coding: utf-8 -*-

class ProductAPI(object):

    def list_products(self, *args, **kwargs):
        url = self.base_url + "products"
        contents = self.get(url, **kwargs)
        return contents

    def get_product(self, id):
        url = self.base_url + "products/%s" % id
        contents = self.get(url)
        return contents
