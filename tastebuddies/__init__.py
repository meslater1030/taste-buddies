from pyramid.config import Configurator
from sqlalchemy import engine_from_config

import os

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from cryptacular.bcrypt import BCRYPTPasswordManager

from .models import (
    DBSession,
    Base,
)

from security import groupfinder, UserFactory

# for group in self.user_groups:
#             acl.append((Allow, 'group:{}'.format(group.id), 'view'))


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    auth_secret = os.environ.get('TASTEBUDDIES_AUTH_SECRET', 'tastynoms')

    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512',
        callback=groupfinder,
    )

    authz_policy = ACLAuthorizationPolicy()

    settings['auth.username'] = os.environ.get('AUTH_USERNAME', 'admin')
    manager = BCRYPTPasswordManager()
    settings['auth.password'] = os.environ.get(
        'AUTH_PASSWORD', manager.encode('secret')
    )

    config = Configurator(
        settings=settings,
        authentication_policy=authn_policy,
        authorization_policy=authz_policy,
    )

    config.include('pyramid_jinja2')
    config.include('pyramid_tm')

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('user_create', '/create_user')
    config.add_route('user_login', '/login')

    config.add_route('verify', '/verify')
    config.add_route('send_email', '/send_email')
    config.add_route('logout', '/logout')
    config.add_route('profile_detail', '/profile/{username}',
                     factory=UserFactory, traverse='/{username}')
    config.add_route('profile_edit', '/profile/edit/{username}')
    config.add_route('group_create', '/group/create_group')
    config.add_route('group_detail', '/group/{group_id}')
    config.add_route('group_edit', '/group/edit/{group_id}')
    config.add_route('group_forum', '/group/{group_id}/{}')

    config.scan()

    return config.make_wsgi_app()
