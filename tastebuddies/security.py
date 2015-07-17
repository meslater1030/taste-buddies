# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyramid.security import Allow, Authenticated
from models import DBSession, User, Group


def groupfinder(uname, request):
    user = User.lookup_user_by_username(uname)

    acls = []

    if user:
        for group in user.user_groups:
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
