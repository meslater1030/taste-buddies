# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import models
import os
import pytest
from sqlalchemy import create_engine

TEST_DATABASES_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql:///test-taste-buddies'
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
    taste_list = ['sweet', 'salty', 'spicy']
    for tastes in taste_list:
        models.Profile.write(
            taste=tastes
        )
    models.AgeGroup.write(
        age_group='18-24'
    )
    models.Location.write(
        city='Seattle'
    )
    models.Cost.write(
        cost='expensive'
    )
    models.Diet.write(
        diet='vegan'
    )
    user = models.User.write(
        username='BobRocks',
        firstname='Bob',
        lastname='Jones',
        password='secret',
        email='bob.jones@gmail.com',
        restaurants='Chipotle',
    )
    user2 = models.User.write(
        username='pewpew',
        firstname='Bob',
        lastname='Jones',
        password='secret',
        email='pewpew@gmail.com',
        restaurants='Chipotle',
    )
    salty = db_session.query(models.Profile).all()[1]
    user.food_profile.append(salty)
    user2.food_profile.append(salty)
    db_session.flush()


def test_create_user(create_user, db_session):
    create_user
    assert len(db_session.query(models.User).all()) == 2
    assert len(db_session.query(models.Diet).all()) == 1
    assert len(db_session.query(models.Profile).all()) == 3
    assert len(db_session.query(models.Location).all()) == 1
    assert len(db_session.query(models.Cost).all()) == 1
    assert len(db_session.query(models.AgeGroup).all()) == 1
