from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

import os

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib
from random import randint

from pyramid.security import remember, forget
from cryptacular.bcrypt import BCRYPTPasswordManager

from models import (User, Cost, Location, AgeGroup, Profile, Post, Discussion,
                    Group, Diet)


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

            User.write(
                username=username,
                password=hashed,
                email=email,
                cost=1,
                age=1,
                user_location=1
            )
            headers = remember(request, username)

            return HTTPFound(request.route_url('send_email'), headers=headers)
        except:
            return {}
    return {'username': username}


@view_config(route_name='send_email')
def send_verify_email(request):

    ver_code = randint(1000, 9999)

    uname = request.authenticated_userid
    user_obj = User.lookup_user_by_username(uname)
    user_obj.write_ver_code(username=user_obj.username, ver_code=ver_code)

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
             renderer='templates/verify.jinja2')
def verify(request):
    uname = request.authenticated_userid
    user_obj = User.lookup_user_by_username(uname)
    action = {'username': uname}

    if request.method == "POST":
        user_vcode = int(request.params.get('verify_code'))
        db_vcode = user_obj.ver_code

        if user_vcode == db_vcode:
            user_obj.confirm_user(username=user_obj.username)

            action = HTTPFound(
                request.route_url('profile_detail', username=uname)
            )

    return action


def do_login(request):
    login_result = False
    manager = BCRYPTPasswordManager()

    entered_username = request.params.get('username', None)
    entered_password = request.params.get('password', None)

    user_obj = User.lookup_user_by_username(username=entered_username)
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
    udata = User.lookup_user_by_username(username)

    try:
        verified_status = udata.confirmed
    except:
        verified_status = False

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
                    username=username),
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

    uname = request.matchdict['username']
    udata = User.lookup_user_by_username(uname)

    tastes = []
    diets = []
    groups = []

    for taste in udata.food_profile:
        tastes.append(taste.taste)

    for diet in udata.diet_restrict:
        diets.append(diet.diet)

    for group in udata.user_groups:
        groups.append(group)

    price = Cost.one(eid=udata.cost).cost
    location = Location.one(eid=udata.user_location).city
    age = AgeGroup.one(eid=udata.age).age_group

    return {
        'username': udata.username,
        'firstname': udata.firstname,
        'lastname': udata.lastname,
        'food': udata.food,
        'restaurant': udata.restaurants,
        'tastes': tastes,
        'diets': diets,
        'groups': groups,
        'age': age,
        'location': location,
        'price': price,
    }


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
            restaurant = request.params.get('favorite_restaurants')
            price = request.params.get('group_price')
            food = request.params.get('favorite_food')
            age = request.params.get('age')
            User.change(username=username, firstname=firstname,
                        lastname=lastname, location=location,
                        taste=taste, diet=diet, price=price,
                        restaurant=restaurant, food=food, age=age)

            headers = remember(request, username)
            return HTTPFound(request.route_url(
                             'profile_detail', username=username
                             ),
                             headers=headers)

    username = request.authenticated_userid
    user = User.lookup_user_by_username(username)
    tastes = Profile.all()
    diet = Diet.all()
    age = AgeGroup.all()
    location = Location.all()
    price = Cost.all()
    return {'user': user, 'tastes': tastes, 'ages': age, 'location': location,
            'price': price, 'username': username, 'diets': diet}


@view_config(route_name='group_create',
             renderer='templates/group_create.jinja2')
def group_create_view(request):
    username = request.authenticated_userid

    if request.method == 'POST':
            group_name = request.params.get('group_name')
            group_descrip = request.params.get('group_description')
            location = request.params.get('location')
            taste = request.params.getall('personal_taste')
            diet = request.params.getall('diet')
            price = request.params.get('group_price')
            age = request.params.get('age')
            Group.write(name=group_name, description=group_descrip,
                        location=location, food_profile=taste,
                        diet_restrict=diet, cost=price, age=age,
                        Admin=username)
            all_groups = Group.all()
            for group in all_groups:
                if group.name == group_name:
                    group_id = group.id
            return HTTPFound(request.route_url('group_detail',
                             group_id=group_id))
    tastes = Profile.all()
    diet = Diet.all()
    age = AgeGroup.all()
    location = Location.all()
    price = Cost.all()
    return {
        'username': username,
        'tastes': tastes,
        'ages': age,
        'location': location,
        'price': price,
        'diets': diet
    }


@view_config(route_name='group_detail',
             renderer='templates/group_detail.jinja2')
def group_detail_view(request):
    group = Group.lookup_group_by_id(request.matchdict['group_id'])
    members = User.all()
    group_members = []
    for member in members:
        for group in member.user_groups:
            if group == member.user_groups:
                group_members.append(group)

    price = Cost.one(eid=group.cost).cost
    location = Location.one(eid=group.location).city
    age = AgeGroup.one(eid=group.age).age_group
    return {'group': group, 'members': members,
            'age': age, 'location': location, 'price': price}


@view_config(route_name='group_edit',
             renderer='templates/group_edit.jinja2')
def group_edit_view(request):
    username = request.authenticated_userid
    if request.method == 'POST':
        group_name = request.params.get('group_name')
        group_descrip = request.params.get('group_description')
        location = request.params.get('location')
        taste = request.params.getall('personal_taste')
        diet = request.params.getall('diet')
        price = request.params.get('group_price')
        age = request.params.get('age')
        Group.write(name=group_name, description=group_descrip,
                    location=location, food_profile=taste,
                    diet_restrict=diet, cost=price, age=age,
                    Admin=username)
        all_groups = Group.all()
        for group in all_groups:
            if group.name == group_name:
                group_id = group.id
        return HTTPFound(request.route_url('group_detail',
                         group_id=group_id))
    group = Group.lookup_group_by_id(request.matchdict['group_id'])
    ages = AgeGroup.all()
    locations = Location.all()
    food_profiles = Profile.all()
    diets = Diet.all()
    costs = Cost.all()
    return {'group': group, 'ages': ages,
            'locations': locations, 'food_profiles': food_profiles,
            'diets': diets, 'costs': costs}


@view_config(route_name='group_forum',
             renderer='templates/group_forum.jinja2')
def group_forum_view(request):
    """
    If the request method is POST then writes either the discussion or
    the post to the database.
    If the request method is GET finds the appropriate group and its
    associated discussions.  creates an ordered dictionary with the
    discussion title as key and the post texts as values in a list.
    Reverses the ordered dictionary so that the most recent discussions
    appear first.
    """
    group = Group.lookup_group_by_id(request.matchdict['group_id'])

    if request.method == 'POST':
        if request.params.get('title'):
            title = request.params.get('title')
            Discussion.write(title=title, group_id=group.id)
        if request.params.get('text'):
            discussion = Discussion.one(request.matchdict['discussion_id'])
            text = request.params.get('text')
            Post.write(text=text, discussion_id=discussion.id)

    discussions = group.discussions
    posts = discussions.posts
    return {'discussions': discussions, 'posts': posts}


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
