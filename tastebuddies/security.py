# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyramid.security import Allow, Authenticated, ALL_PERMISSIONS


class RootFactory(object):
    __acl__ = [
        (Allow, Authenticated, ALL_PERMISSIONS)
    ]

    def __init__(self, request):
        self.request = request
