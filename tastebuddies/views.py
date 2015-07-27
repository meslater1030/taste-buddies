from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPForbidden

import os

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib
from random import randint

from pyramid.security import remember, forget
from cryptacular.bcrypt import BCRYPTPasswordManager

from models import (User, Post, Discussion,
                    Group, Criteria)


@view_config(route_name='home',
             renderer='templates/home.jinja2')
def home_view(request):
    return {'username': request.authenticated_userid}


@view_config(route_name='user_create',
             renderer='templates/user_create.jinja2')
def user_create_view(request):

    username = request.authenticated_userid

    if request.method == 'POST':

        try:
            manager = BCRYPTPasswordManager()
            username = request.params.get('username')
            password = request.params.get('password')
            hashed = manager.encode(password)
            email = request.params.get('email')
            user = User.add(
                username=username,
                password=hashed,
                email=email,
            )
            Criteria.add(user=user)
            headers = remember(request, username)

            return HTTPFound(request.route_url('send_email'), headers=headers)
        except:
            return {}
    return {'username': username}


@view_config(route_name='send_email', permission='authn')
def send_verify_email(request):

    ver_code = randint(1000, 9999)

    uname = request.authenticated_userid
    user_obj = User.lookup_by_attribute(username=uname)[0]
    user_obj.write_ver_code(username=user_obj.username,
                            ver_code=ver_code)

    fromaddr = "tastebot@gmail.com"
    toaddr = user_obj.email

    msg = MIMEMultipart()
    msg["From"] = fromaddr
    msg["To"] = toaddr
    msg["Subject"] = "Your Tastebuddies Verification Code"

    body = ''

    here = os.path.dirname(os.path.abspath(__file__))
    email_directory = os.path.join(here, 'static', 'email_templates')
    body_template = os.path.join(email_directory, 'body.txt')
    with open(body_template, 'r') as fh:
        body = str(fh.read())

    body = body.format(ver_code=ver_code)

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("tastebot", 'TASTEBUDDIES')
    text = msg.as_string()

    server.sendmail(fromaddr, toaddr, text)

    return HTTPFound(request.route_url('verify'))


@view_config(route_name='verify',
             permission='authn',
             renderer='templates/verify.jinja2')
def verify(request):
    error_msg = None
    uname = request.authenticated_userid
    user_obj = User.lookup_by_attribute(username=uname)[0]

    if request.method == "POST":
        user_vcode = int(request.params.get('verify_code'))
        db_vcode = user_obj.ver_code

        if user_vcode == db_vcode:
            user_obj.confirm_user(username=user_obj.username)

            action = HTTPFound(
                request.route_url('profile_detail', username=uname)
            )

    action = {'username': uname, 'error_msg': error_msg}

    return action


def do_login(request):
    login_result = False
    manager = BCRYPTPasswordManager()

    entered_username = request.params.get('username', None)
    entered_password = request.params.get('password', None)

    user_obj = User.lookup_by_attribute(username=entered_username)[0]
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
    username = request.params.get('username', None)
    udata = User.lookup_by_attribute(username=username)[0]

    try:
        verified_status = udata.confirmed
    except:
        verified_status = False

    return verified_status


@view_config(route_name='user_login',
             renderer='templates/login.jinja2')
def login(request):
    error_msg = None
    username = request.params.get('username', '')
    result = None

    if request.method == 'POST':
        error_msg = 'Login Failed'
        authn = False

        try:
            authn = passes_authentication(request)

        except ValueError as e:
            error_msg = str(e)

        if authn is True:
            headers = remember(request, username)

            if passes_verification(request):
                result = HTTPFound(request.route_url(
                    'profile_detail',
                    username=username),
                    headers=headers,
                )
            else:
                result = HTTPFound(request.route_url(
                    'verify'),
                    headers=headers,
                )

    if not result:
        result = {'error_msg': error_msg, 'username': username}

    return result


@view_config(route_name='logout', permission='authn')
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)


@view_config(route_name='profile_detail',
             renderer='templates/profile_detail.jinja2')
def profile_detail_view(request):
    if not (request.has_permission('owner')
            or request.has_permission('connect')):
        return HTTPForbidden()

    user = User.lookup_by_attribute(username=request.matchdict['username'])[0]
    profile = {}
    profile['username'] = request.authenticated_userid,
    profile['user'] = user
    profile['criteria'] = Criteria.lookup_by_attribute(user=user)[0]
    return profile


@view_config(route_name='profile_edit',
             permission='authn',
             renderer='templates/profile_edit.jinja2')
def profile_edit_view(request):
    username = request.authenticated_userid
    user = User.lookup_by_attribute(username=username)[0]
    criteria = Criteria.lookup_by_attribute(user=user)[0]
    if request.method == 'POST':
        User.edit(id=user.id,
                  username=username,
                  firstname=request.params.get('first_name'),
                  lastname=request.params.get('last_name'),
                  restaurants=request.params.get('favorite_restaurants'),
                  food=request.params.get('favorite_food')
                  )
        Criteria.edit(id=criteria.id,
                      location=request.params.getall('location'),
                      taste=request.params.getall('taste'),
                      diet=request.params.getall('diet'),
                      cost=request.params.getall('cost'),
                      age=request.params.getall('age')
                      )
        headers = remember(request, username)
        return HTTPFound(request.route_url(
                         'profile_detail', username=username
                         ),
                         headers=headers)
    profile = {}
    profile['criteria'] = criteria
    profile['username'] = username
    profile['user'] = user
    return profile


@view_config(route_name='group_create',
             permission='authn',
             renderer='templates/group_create.jinja2')
def group_create_view(request):
    username = request.authenticated_userid
    admin = User.lookup_by_attribute(username=username)[0]
    if request.method == 'POST':
        group = Group.add(name=request.params.get('name'),
                          description=request.params.get('description'),
                          admin=admin, users=[admin])
        Criteria.add(location=request.params.getall('location'),
                     taste=request.params.getall('taste'),
                     diet=request.params.getall('diet'),
                     cost=request.params.getall('cost'),
                     age=request.params.getall('age'),
                     group=group)
        return HTTPFound(request.route_url('group_detail',
                         group_name=group.name))
    profile = {}
    profile['criteria'] = Criteria()
    profile['username'] = username
    return profile


@view_config(route_name='group_detail',
             renderer='templates/group_detail.jinja2')
def group_detail_view(request):
    username = request.authenticated_userid
    group = Group.lookup_by_attribute(name=request.matchdict['group_name'])[0]
    criteria = Criteria.lookup_by_attribute(group=group)[0]
    if request.method == 'POST':
        user = User.lookup_by_attribute(username=username)[0]
        user.groups.append(group)
        return HTTPFound(request.route_url(
                         'group_detail',
                         group_id=request.matchdict['group_id'],
                         ))
    profile = {}
    profile['criteria'] = criteria
    profile['group'] = group
    profile['username'] = username
    return profile


@view_config(route_name='group_forum',
             renderer='templates/group_forum.jinja2')
def group_forum_view(request):
    username = request.authenticated_userid
    group = Group.lookup_by_attribute(name=request.matchdict['group_name'])[0]
    criteria = Criteria.lookup_by_attribute(group=group)[0]
    if request.method == 'POST':
        user = User.lookup_by_attribute(username=username)[0]
        user.groups.append(group)
        if request.params.get('title'):
            title = request.params.get('title')
            Discussion.add(title=title, group_id=group.id)
        if request.params.get('text'):
            discussion = (Discussion.lookup_by_attribute(
                          id=request.matchdict['discussion_id'])[0])
            text = request.params.get('text')
            Post.add(text=text, discussion_id=discussion.id)
    tmp_discussions = group.discussions
    for discussion in Discussion.all():
        if discussion.group_id == group.id:
            tmp_discussions.append(discussion)
    profile = {}
    profile['discussions'] = []
    for discussion in tmp_discussions:
        profile['discussions'].append(tmp_discussions.pop())
    profile['posts'] = Post.all()
    profile['group'] = group
    profile['username'] = username
    profile['criteria'] = criteria

    return profile


@view_config(route_name='group_edit',
             permission='authn',
             renderer='templates/group_edit.jinja2')
def group_edit_view(request):
    username = request.authenticated_userid
    group = Group.lookup_by_attribute(name=request.matchdict['group_name'])[0]
    criteria = Criteria.lookup_by_attribute(group=group)[0]
    if request.method == 'POST':
        criteria = Criteria.edit(location=request.params.getall('location'),
                                 taste=request.params.getall('taste'),
                                 diet=request.params.getall('diet'),
                                 cost=request.params.getall('cost'),
                                 age=request.params.getall('age'),
                                 id=criteria.id)
        group = Group.edit(name=request.params.get('name'),
                           description=request.params.get('description'),
                           id=group.id)
        return HTTPFound(request.route_url('group_detail',
                                           group_name=group.name))

    profile = {}
    profile['criteria'] = criteria
    profile['group'] = group
    profile['username'] = username

    return profile


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
