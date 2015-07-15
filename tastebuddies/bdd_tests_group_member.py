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


@given('a group member')
def test_group_member():
    # login admin
    url = ("http://ec2-52-27-184-229.us-west-2."
           "compute.amazonaws.com/login")
    browser.visit(url)
    browser.find_by_name('username')[0].type('admin')
    browser.find_by_name('password')[0].type('secret')
    browser.find_by_name('submit')[0].click()
    url = ("http://ec2-52-27-184-229.us-west-2."
           "compute.amazonaws.com/group/create_group")
    browser.visit(url)
    # admin creates group
    browser.find_by_name('group_name')[0].type('Spicy Food Lovers')
    browser.select('age_range', '18-24')
    browser.select('location', 'Eastside')
    browser.find_by_value('Spicy').check
    browser.find_by_value('Barbecue').check
    browser.find_by_value('Mexican').check
    browser.choose('group_price', 'cheap')
    browser.find_by_name('profile_save')[0].click()
    # admin logs out
    browser.find_by_name('logout')[0].click()
    # admin2 logs in
    browser.find_by_name('username')[0].type('admin2')
    browser.find_by_name('password')[0].type('secret')
    browser.find_by_name('submit')[0].click()
    browser.visit('http://ec2-52-27-184-229.us-west-2'
                  '.compute.amazonaws.com/group/1')
    # admin 2 joins group
    browser.find_by_name('join')[0].click()


@scenario('features/groups.feature', 'Leaving Groups')
def test_leaving_groups():
    pass


@when('I visit a group page')
def test_group_view():
    url = ('http://ec2-52-27-184-229.us-west-2'
           '.compute.amazonaws.com/group/1')
    browser.visit(url)


@then('I can leave that group')
def test_leave_group():
    assert browser.is_element_present_by_name('leave')
    browser.find_by_name('leave')[0].click()


@then('I cannot see group posts')
def test_not_view_group_posts():
    url = ('http://ec2-52-27-184-229.us-west-2'
           '.compute.amazonaws.com/group/1')
    browser.visit(url)
    assert not browser.is_text_present('forum')


@scenario('features/groups.feature', 'Post in Groups')
def test_post_groups():
    pass


@scenario('features/groups.feature', 'View Group Members')
def test_view_group_members():
    pass


@then('I will be able to see all the members of my group')
def test_see_group_members():
    # update with group members id or class or whatever
    assert browser.find_by_id('group_members')[0].is_text_present('')


@then('I will be able to write a post')
def test_write_post():
    # this needs to be updated for the name of the post/title?
    browser.find_by_name('post')[0].type('Spicy food is awesome!')


@then('that post will be visible to other group members')
def test_post_visible():
    browser.find_by_name('logout')[0].click()
    browser.find_by_name('login')[0].click()
    browser.find_by_name('username')[0].type('admin')
    browser.find_by_name('password')[0].type('secret')
    browser.find_by_name('submit')[0].click()
    browser.visit('http://ec2-52-27-184-229.us-west-2'
                  '.compute.amazonaws.com/group/1')
    assert browser.is_text_present('Spicy food is awesome!')


@scenario('features/groups.feature', 'Delete Group Posts')
def test_delete_group_posts():
    pass


@when('I have created a post')
def test_create_post():
    # this needs to be updated with name of post/title
    browser.find_by_name('post')[0].type('Something Regrettable')


@then('I will be able to delete my post')
def test_delete_my_post():
    # this needs to be updated with the delete plus a way
    # to find that specific post
    browser.find_by_name('delete')[0].click()


@then('that post will not exist')
def test_post_deleted():
    assert not browser.is_text_present('Something Regrettable')
