# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from models import User, DBSession


def groupfinder(uname, request):
    user = User.lookup_user_by_username(uname)

    acls = []

    if user:
        for group in user.user_groups:
            acls.append('group:{}'.format(group.id))

    return acls


class UserFactory(object):
    def __init__(self, request):
        self.request = request

    def __getitem__(self, key):
        return DBSession.query(User).filter(User.username == key).one()
