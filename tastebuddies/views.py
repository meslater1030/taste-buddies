from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from pyramid.security import remember, forget
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    # MyModel,
)


# @view_config(route_name='home', renderer='templates/test.jinja2')
# def my_view(request):
#     try:
#         one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
#     except DBAPIError:
#         return Response(conn_err_msg, content_type='text/plain',
#                         status_int=500)
#     return {'one': one, 'project': 'tastebuddies'}

@view_config(route_name='home',
             renderer='templates/home.jinja2')
def home_view(request):
    return {}


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)


@view_config(route_name='user_create',
             renderer='templates/user_create.jinja2')
def user_create_view(request):
    return {}


@view_config(route_name='verify',
             renderer='templates/verify.jinja2')
def verify(request):
    return {}


@view_config(route_name='profile_create',
             renderer='templates/profile_create.jinja2')
def profile_create_view(request):
    return {}


@view_config(route_name='user_login',
             renderer='templates/login.jinja2')
def login(request):
    return {}


@view_config(route_name='profile_detail',
             renderer='templates/profile_detail.jinja2')
def profile_detail_view(request):
    return {}


@view_config(route_name='profile_edit',
             renderer='templates/profile_edit.jinja2')
def profile_edit_view(request):
    return {}


@view_config(route_name='group_create',
             renderer='templates/group_create.jinja2')
def group_create_view(request):
    return {}


@view_config(route_name='group_detail',
             renderer='templates/group_detail.jinja2')
def group_detail_view(request):
    return {}


@view_config(route_name='group_edit',
             renderer='templates/group_edit.jinja2')
def group_edit_view(request):
    return {}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_tastebuddies_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
