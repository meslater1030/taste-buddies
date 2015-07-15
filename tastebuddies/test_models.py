# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import models
import os
import pytest
from sqlalchemy import create_engine

TEST_DATABASES_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql:///tastebuddies'
)
os.environ['DATABASE_URL'] = TEST_DATABASES_URL


# you will want to make a fixture that creates an app

@pytest.fixture(scope='session')
def connection(request):
    engine = create_engine(TEST_DATABASES_URL)
    models.Base.metadata.create_all(engine)
    connection = engine.connect()
    models.DBSession.registry.clear()
    models.DBSession.configure(bind=connection)
    models.Base.metadata.bind = engine
    request.addfinalizer(models.Base.metadata.drop_all)
    return connection


@pytest.fixture()
def db_session(request, connection):
    from transaction import abort
    trans = connection.begin()
    request.addfinalizer(trans.rollback)
    request.addfinalizer(abort)

    from models import DBSession
    return DBSession


@pytest.fixture()
def create_user(db_session):
    models.User.write(
        username='BobRocks',
        firstname='Bob',
        lastname='Jones',
        password='secret',
        email='bob.jones@gmail.com',
        restaurants='Chipotle',
        )
    models.User.write(
        username='pewpew',
        firstname='Bob',
        lastname='Jones',
        password='secret',
        email='pewpew@gmail.com',
        restaurants='Chipotle',
        )
    models.User.write(
        username='imdabest',
        firstname='Bob',
        lastname='Jones',
        password='secret',
        email='imthebest@gmail.com',
        restaurants='Chipotle',
        )

def test_create_user(create_user, db_session):
    create_user
    import pdb;pdb.set_trace()
