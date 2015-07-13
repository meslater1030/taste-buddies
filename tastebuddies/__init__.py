from pyramid.config import Configurator
from sqlalchemy import engine_from_config

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
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('pyramid_tm')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('user_create', '/create_user')
    config.add_route('verify', '/verify')
    config.add_route('profile_create', '/create_profile')
    config.add_route('user_login', '/login')
    config.add_route('profile_detail', '/profile/{username}')
    config.add_route('profile_edit', '/profile/edit/{profile_id}')
    config.add_route('group_create', '/group/create_group')
    config.add_route('group_detail', '/group/{group_id}')
    config.add_route('group_edit', '/group/edit/{group_id}')
    config.scan()
    return config.make_wsgi_app()
