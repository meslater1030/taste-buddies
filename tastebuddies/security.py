# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyramid.security import Allow, Authenticated
from models import DBSession, User, Group


def groupfinder(uname, request):
    user = User.lookup_by_attribute(username=uname)[0]

    acls = []

    if user:
        for group in user.groups:
            acls.append('group:{}'.format(group.id))

    return acls


class Root(object):
    __acl__ = [
        (Allow, Authenticated, 'authn'),
    ]

    def __init__(self, request):
        self.request = request


class UserFactory(object):
    def __init__(self, request):
        self.request = request

    def __getitem__(self, key):
        return DBSession.query(User).filter(User.username == key).one()


class GroupFactory(object):
    def __init__(self, request):
        self.request = request

    def __getitem__(self, key):
        return DBSession.query(Group).filter(Group.id == key).one()
