[![Travis](https://travis-ci.org/meslater1030/taste-buddies.svg)](https://travis-ci.org/meslater1030/taste-buddies.svg)

# taste-buddies
**TasteBuddies** lets you connect to people who like the food you like!


# IMPORTANT

**Make sure to run `python setup.py develop` after pulling down from
GitHub. This will create the system-specific egg files for gunicorn,
etc. to use.**


### User Story's for taste buddies:
- As a Prospective User, I want to creat an account.
- As a Prospective User, I want to view existing groups.
- As a User, I want to edit profile.
- As a User, I want to join groups.
- As a User, I want to leave groups.
- As a User, I want to receive group suggestions.
- As a User, I want to create a profile that includes my photo and taste
preferences.
- As a User, I want to be redirected to my profile after I logged in.
- As a User, I want to create food groups and become group admin of the group
- As a Group Member, I want to write posts.
- As a Group Member, I want to delete my own posts.
- As a Group Member, I want to view profiles of other users in the group.
- As a Group Admin, I want to delete posts.
- As a Group Admin, I want to delete group.
- As a Group Admin, I want to have existing group member's power.
- As a Group Admin, I want to create and edit group profile.
- As a Group Admin, I want to boot users from group.


## Collaborators:

- [Karen Wong](https://github.com/kaka0525)
- [Megan Slater](https://github.com/meslater1030)
- [Johnson Jew](https://github.com/johnsonjew)
- [Tanner Lake](https://github.com/tlake)


## Notes:

##### Running the Server
Starting the server will be accomplished with either of the following
commands:
`gunicorn --paste production.ini` for the production server, and
`gunicorn --paste development.ini` when developing.


##### The Filesystem / Project Tree

The `main` function (which contains things like `config.include()` and
`config.add_route()`) lives inside of the `__init__.py` file in the
lowest-level `tastebuddies` directory; this file is situated next to the
`static` and `templates` directories, and next to the `models.py` and
`views.py` files.

Most of rest of the project tree should make sense. The `@view_config`
functions live inside of `views.py`, and models are defined within `models.py`.
Jinja2 templates will live inside the `templates` directory, and static files
like images and stylesheets go in the `static` directory.

The low-level `tastebuddies` project root directory is contained within
another upper-level `tastebuddies` directory, which houses things that are,
essentially, wrappings for our project. Here we'll find things like our
`README.md` and `requirements.txt` files. There also exist some new files:

- `development.ini` and `production.ini`
    - These two files are used to configure our server when we want to start
    it up. They allow us to have a different environment depending on our
    situation (for example, `development.ini` includes a debugging toolbar
    which is helpful, but would allow any old user to fuss around in our
    system, so we don't want it in the production environment).

- `setup.py`
    - This is used to create a `.egg-info` directory which contains a bunch
    of system-specific configurations. That directory isn't anything we'll
    need to be dealing with, but we will need it in order to run the server
    properly. So, when we pull down from GitHub, we'll want to be sure that
    we run `python setup.py develop` to populate the `.egg-info` directory,
    and then we can run the `gunicorn --paste` command to start up the server.
    Additionally, that `.egg-info` directory is not anything that we want to
    track with Git; our `.gitignore` is configured to take care of that.