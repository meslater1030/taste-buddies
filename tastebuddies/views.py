from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
# import models as m

from pyramid.security import remember, forget, Authenticated
from cryptacular.bcrypt import BCRYPTPasswordManager

from models import User


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
    if request.method == 'POST':
        try:
            manager = BCRYPTPasswordManager()

            username = request.params.get('username')
            password = request.params.get('password')
            email = request.params.get('email')

            hashed = manager.encode(password)

            User.write(username=username, password=hashed, email=email)

            headers = remember(request, username)
            return HTTPFound(request.route_url('verify'), headers=headers)
        except:
            return {}
    return {}


@view_config(route_name='verify',
             renderer='templates/verify.jinja2')
def verify(request):
    action = {}

    if request.method == "POST":
        vcode = request.params.get('verify_code')
        if vcode == 1234:
            uid = request.authenticated_userid
            action = HTTPFound(
                request.route_url('profile_detail', username=uid)
            )

    return action


def do_login(request):
    # import pdb; pdb.set_trace()
    login_result = False
    manager = BCRYPTPasswordManager()

    entered_username = request.params.get('username', None)
    entered_password = request.params.get('password', None)

    user_obj = User.lookup_user(username=entered_username)
    db_username = user_obj.username

    if entered_username == db_username:
        db_hashed = user_obj.password
        # manager.check returns BOOL
        login_result = manager.check(db_hashed, entered_password)

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
            import pdb; pdb.set_trace()
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


@view_config(route_name='logout',)
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)


@view_config(route_name='profile_detail',
             renderer='templates/profile_detail.jinja2')
def profile_detail_view(request):
    return {}


@view_config(route_name='profile_edit',
             renderer='templates/profile_edit.jinja2')
def profile_edit_view(request):
    if request.method == 'POST':
            username = request.authenticated_userid
            firstname = request.params.get('first_name')
            lastname = request.params.get('last_name')
            location = request.params.get('location')
            taste = request.params.getall('personal_taste')
            diet = request.params.getall('diet')
            restaurant = request.params.get('restaurant')
            price = request.params.get('group_price')
            User.change(username=username, firstname=firstname,
                        lastname=lastname, location=location,
                        taste=taste, diet=diet, price=price,
                        restaurant=restaurant)
            headers = remember(request, username)
            return HTTPFound(request.route_url('verify'), headers=headers)
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
