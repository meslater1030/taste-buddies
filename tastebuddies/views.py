from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from pyramid.security import remember, forget, Authenticated
from cryptacular.bcrypt import BCRYPTPasswordManager

from models import Discussion, Post

from collections import OrderedDict


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


@view_config(route_name='user_create',
             renderer='templates/user_create.jinja2')
def user_create_view(request):
    return {}


@view_config(route_name='verify',
             permission=Authenticated,
             renderer='templates/verify.jinja2')
def verify(request):
    return {}


@view_config(route_name='profile_create',
             permission=Authenticated,
             renderer='templates/profile_create.jinja2')
def profile_create_view(request):
    return {}


def do_login(request):
    username = request.params.get('username', None)
    password = request.params.get('password', None)
    login_result = False

    settings = request.registry.settings
    manager = BCRYPTPasswordManager()

    if username == settings.get('auth.username', ''):
        hashed = settings.get('auth.password', '')
        # manager.check returns bool
        login_result = manager.check(hashed, password)

    return login_result


def passes_authentication(request):
    username = request.params.get('username', None)
    password = request.params.get('password', None)

    if not (username and password):
        raise ValueError('Both username and password are required')

    return do_login(request)


def passes_verification(request):
    # !!!!!
    # HERE WE NEED TO CHECK THE USER'S 'VERIFIED' DB COLUMN
    # AND RETURN IT
    # !!!!!
    verified_status = True
    return verified_status


@view_config(route_name='user_login',
             renderer='templates/login.jinja2')
def login(request):
    username = request.params.get('username', '')
    error = ''
    result = ''

    if request.method == 'POST':
        error = 'Login Failed'
        authn = False

        try:
            authn = passes_authentication(request)

        except ValueError as e:
            error = str(e)

        if authn is True:
            headers = remember(request, username)
            if passes_verification(request):
                result = HTTPFound(request.route_url(
                    'profile_detail',
                    username='1'),
                    headers=headers,
                )
            else:
                result = HTTPFound(request.route_url(
                    'verify'),
                    headers=headers,
                )

    if not result:
        result = {'error': error, 'username': username}

    return result


@view_config(route_name='logout',
             permission=Authenticated,)
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)


@view_config(route_name='profile_detail',
             permission=Authenticated,
             renderer='templates/profile_detail.jinja2')
def profile_detail_view(request):
    return {}


@view_config(route_name='profile_edit',
             permission=Authenticated,
             renderer='templates/profile_edit.jinja2')
def profile_edit_view(request):
    return {}


@view_config(route_name='group_create',
             permission=Authenticated,
             renderer='templates/group_create.jinja2')
def group_create_view(request):
    return {}


@view_config(route_name='group_detail',
             permission=Authenticated,
             renderer='templates/group_detail.jinja2')
def group_detail_view(request):
    """Pulls all discussions for this group and posts from the database.
    Orders the disucssions according to when they began.
    Associates all posts to the appropriate discussion.
    Sorts the posts in reverse chronological order.
    Reverses the ordered dictionary so that the most recent
    discussions appear first.  Returns a list.
    """
    id = request.matchdict['group_id']
    tmp = OrderedDict()
    discussions = Discussion.group_lookup(id)
    posts = Post.group_lookup()
    forum = OrderedDict()
    for discussion in discussions:
        tmp[discussion.id] = []
    for post in posts:
        tmp[post.discussionpost].append((post.created, post.post_text))
    for i in range(1, len(tmp)-1):
        tmp[i].sort(reverse=True)
    for id in tmp.iterkeys():
        for discussion in discussions:
            if id == discussion.id:
                forum[discussion.discussion_title] = tmp[id]
                del tmp[id]
    final_forum = []
    for i in range(len(forum)):
        final_forum.append(forum.popitem(last=True))
    return final_forum


@view_config(route_name='group_forum',
             permission=Authenticated,
             renderer='templates/group_forum.jinja2')
def group_forum_view(request):
    # Enters posts and/or discussions into the database
    if request.method == 'POST':
        if request.params.get('title'):
            title = request.params.get('title')
            Discussion.write(title=title)
        if request.params.get('text'):
            text = request.params.get('text')
            Post.write(text=text)
    return HTTPFound(request.route_url('group_detail'))


@view_config(route_name='group_edit',
             permission=Authenticated,
             renderer='templates/group_edit.jinja2')
def group_edit_view(request):
    return {}


conn_err_msg = """
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
