# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest
from sqlalchemy import create_engine
from pyramid import testing
from cryptacular.bcrypt import BCRYPTPasswordManager

import tastebuddies


# DB_USR = os.environ.get("USER", )

TEST_DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql:///travis_ci_test'
)
os.environ['DATABASE_URL'] = TEST_DATABASE_URL
os.environ['TESTING'] = 'True'
