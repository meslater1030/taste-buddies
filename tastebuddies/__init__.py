from pyramid.config import Configurator
from sqlalchemy import engine_from_config

import os

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from cryptacular.bcrypt import BCRYPTPasswordManager

from security import RootFactory

from .models import (
    DBSession,
    Base,
)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    settings['auth.username'] = os.environ.get('AUTH_USERNAME', 'admin')
    manager = BCRYPTPasswordManager()
    settings['auth.password'] = os.environ.get(
        'AUTH_PASSWORD', manager.encode('secret')
    )

    auth_secret = os.environ.get('TASTEBUDDIES_AUTH_SECRET', 'tastynoms')

    config = Configurator(
        settings=settings,
        authentication_policy=AuthTktAuthenticationPolicy(
            secret=auth_secret,
            hashalg='sha512',
        ),
        authorization_policy=ACLAuthorizationPolicy(),
    )

    config.include('pyramid_jinja2')
    config.include('pyramid_tm')

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('user_create', '/create_user')
    config.add_route('user_login', '/login')

    config.add_route('verify', '/verify')
    config.add_route('logout', '/logout',
                     factory=RootFactory)
    config.add_route('profile_detail', '/profile/{username}',
                     factory=RootFactory)
    config.add_route('profile_edit', '/profile/edit/{username}',
                     factory=RootFactory)
    config.add_route('group_create', '/group/create_group',
                     factory=RootFactory)
    config.add_route('group_detail', '/group/{group_id}',
                     factory=RootFactory)
    config.add_route('group_edit', '/group/edit/{group_id}',
                     factory=RootFactory)

    config.scan()

    return config.make_wsgi_app()
