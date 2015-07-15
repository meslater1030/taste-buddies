# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pytest_bdd import given, when, then, scenario
from splinter import Browser
import os

browser = Browser()


TEST_DATABASES_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://meslater:@localhost:5432/test-taste-buddies'
)
os.environ['DATABASE_URL'] = TEST_DATABASES_URL
os.environ['TESTING'] = "True"


@scenario('features/public.feature', 'Signing up')
def test_signing_up():
    pass


@given('anyone on the web', scope='module')
def test_annon():
    url = ("http://ec2-52-27-184-229.us-west-2."
           "compute.amazonaws.com/login")
    browser.visit(url)
    browser.find_by_name('username')[0].type('admin')
    browser.find_by_name('password')[0].type('secret')
    browser.find_by_name('submit')[0].click()
    url = ("http://ec2-52-27-184-229.us-west-2."
           "compute.amazonaws.com/group/create_group")
    browser.visit(url)
    browser.find_by_name('group_name')[0].type('Spicy Food Lovers')
    browser.select('age_range', '18-24')
    browser.select('location', 'Eastside')
    browser.find_by_value('Spicy').check
    browser.find_by_value('Barbecue').check
    browser.find_by_value('Mexican').check
    browser.choose('group_price', 'cheap')
    browser.find_by_name('profile_save')[0].click()
    browser.find_link_by_partial_href('logout')[0].click()


@when('I go to the signup page')
def test_signup_view():
    url = ("http://ec2-52-27-184-229.us-west-2.compute"
           ".amazonaws.com/create_user")
    browser.visit(url)


@then('I can create an account')
def test_create_account():
    browser.find_by_name('username')[0].type('JohnsonJew')
    browser.find_by_name('password')[0].type('12345')
    browser.find_by_name('email')[0].type('johnsonjew@gmail.com')
    browser.find_by_name('submit')[0].click()


@then('I can log in')
def test_login_privilege():
    browser.find_link_by_partial_href('logout')[0].click()
    browser.find_link_by_partial_href('login')[0].click()
    browser.find_by_name('username')[0].type('JohnsonJew')
    browser.find_by_name('password')[0].type('12345')
    browser.find_by_name('submit')[0].click()
    assert browser.url != ('http://ec2-52-27-184-229.us-west-2'
                           '.compute.amazonaws.com/login')


@scenario('features/public.feature', 'Anonymous View')
def test_anonymous_view():
    pass


@when('I visit a group page')
def test_group_view():
    url = ('http://ec2-52-27-184-229.us-west-2'
           '.compute.amazonaws.com/group/1')
    browser.visit(url)


@then('I can view that group')
def test_group_view_privilege():
    assert browser.is_text_present('Name')
    assert browser.is_text_present('Description')
    assert not browser.is_text_present('join')
    assert not browser.is_text_present('Edit Group')
    assert not browser.is_text_present('Delete Group')
