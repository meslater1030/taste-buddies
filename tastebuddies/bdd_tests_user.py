# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pytest_bdd import scenario, given, when, then
from splinter import Browser
import os


TEST_DATABASES_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://meslater:@localhost:5432/test-taste-buddies'
)
os.environ['DATABASE_URL'] = TEST_DATABASES_URL
os.environ['TESTING'] = "True"
browser = Browser()


@given('a user', scope="module")
def test_user():
    url = ("http://ec2-52-27-184-229.us-west-2.compute."
           "amazonaws.com/login")
    browser.visit(url)
    browser.find_by_name('username')[0].type('admin')
    browser.find_by_name('password')[0].type('secret')
    browser.find_by_name('submit')[0].click()


@scenario('features/profile.feature', 'Editing User Profile')
def test_edit_user_profile():
    pass


@when('I visit my profile')
def test_visit_profile():
    url = ("http://ec2-52-27-184-229.us-west-2.compute."
           "amazonaws.com/profile/1")
    browser.visit(url)


@when('I click the edit profile button')
def test_edit_profile_button():
    browser.click_link_by_partial_href('/profile/edit')


@then('I can edit my profile')
def test_edit_profile():
    browser.find_by_name('first_name')[0].type('Mary Poppins')
    browser.find_by_name('profile_save')[0].click()


@then('profile edits will populate to my page')
def test_populate_user_profile_edits():
    assert browser.is_text_present('Mary Poppins')


@scenario('features/profile.feature', 'Group Suggestions')
def test_group_suggestions():
    pass


@then('I will see suggested groups')
def test_suggested_groups():
    # update with suggested groups id
    assert browser.find_by_id('suggested_groups')[0].is_text_present('')


@when('I log in')
def test_login():
    pass


@scenario('features/profile.feature', 'User Login')
def test_user_login():
    pass


@then('I will be taken to my profile')
def test_profile_redirect():
    assert browser.url == ('http://ec2-52-27-184-229.us-west-2.compute.'
                           'amazonaws.com/profile/1')
