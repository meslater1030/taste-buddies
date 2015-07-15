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


@given('a group admin', scope='module')
def test_group_admin():
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
    # group_member creates an account
    browser.find_by_name('username')[0].type('group_member')
    browser.find_by_name('password')[0].type('12345')
    browser.find_by_name('email')[0].type('groupmember@gmail.com')
    browser.find_by_name('submit')[0].click()
    browser.find_by_name('first_name')[0].type('Group')
    browser.find_by_name('last_name')[0].type('Member')
    browser.select('age_range', '25-34')
    browser.select('location', 'Seattle')
    browser.find_by_value('Salty').check
    browser.find_by_value('Persian').check
    browser.find_by_value('Soul').check
    browser.find_by_value('Vegan').check
    browser.find_by_value('Low_Carb').check
    browser.find_by_name('favorite_restaurants')[0].type('Chipotle')
    browser.find_by_name('favorite_food')[0].type('Corn')
    browser.choose('group_price', 'average')
    browser.find_by_name('profile_save')[0].click()
    # group member joins group
    browser.find_by_name('join')[0].click()
    browser.find_by_name('post')[0].type('Spicy food is awesome!')
    # group member logs out
    browser.find_by_name('logout')[0].click()
    # admin logs back in
    browser.find_by_name('username')[0].type('admin')
    browser.find_by_name('password')[0].type('secret')
    browser.find_by_name('submit')[0].click()


@scenario('features/group_admin.feature', 'Admin Delete Posts')
def test_admin_delete_posts():
    pass


@when('I visit a group page forum')
def test_group_forum():
    url = ("http://ec2-52-27-184-229.us-west-2."
           "compute.amazonaws.com/group/1")
    browser.visit(url)


@then('I will be able to delete any post')
def test_delete_any_post():
    # this needs to be updated with the delete button name or id
    browser.find_by_name('delete')[0].click()
    assert not browser.is_text_present('Spicy food is awesome!')


@scenario('features/group_admin.feature', 'Admin Delete Group')
def test_admin_delete_group():
    pass


@then('I will be able to delete the group')
def test_delete_group():
    url = ("http://ec2-52-27-184-229.us-west-2."
           "compute.amazonaws.com/group/1")
    browser.visit(url)
    browser.find_link_by_partial_text('Delete Group')[0].click()


@then('that group will not exist')
def test_group_deleted():
    # Update with test group or else do a test group fixture
    assert browser.is_text_present('Spicy Food Lovers')


@scenario('features/group_admin.feature', 'Admin authorization')
def test_admin_authorization():
    pass


@then('I will have the same authorizations as any group member')
def test_admin_authorizations():
    # this will need to be updated with forum title/post
    browser.find_by_name('forum')[0].type('I love being an admin!')
    assert browser.is_text_present('I love being an admin!')
    assert browser.find_by_id('group_members')[0].is_text_present('')


@scenario('features/group_admin.feature', 'Admin Edit Group')
def test_admin_edit_group():
    pass


@when('I click the edit group button')
def test_group_button_clicked():
    browser.find_link_by_partial_href('edit')[0].click()


@then('I will be able to edit that group')
def test_edit_group():
    assert "/group/edit" in browser.url
    browser.find_by_name('group_name')[0].type('Spicy Food Haters')
    browser.find_by_name('profile_save')[0].click()


@then('Those edits will be visible to everyone')
def test_group_edits_populate():
    browser.find_link_by_partial_href('logout')[0].click()
    browser.find_link_by_partial_href('login')[0].click()
    browser.find_by_name('username')[0].type('group_member')
    browser.find_by_name('password')[0].type('secret')
    browser.find_by_name('submit')[0].click()
    browser.visit('http://ec2-52-27-184-229.us-west-2'
                  '.compute.amazonaws.com/group/1')
    assert browser.is_text_present('Spicy Food Haters')


@scenario('features/group_admin.feature', 'Admin Delete Group Member')
def test_admin_delete_group_member():
    pass


@then('I will be able to delete a member of the group')
def test_delete_group_member():
    # need to change how we find the user delete
    browser.find_by_name('delete user')[0].click()


@then('that user will no longer be a group member')
def test_group_member_deleted():
    # needs to change from above
    assert not browser.is_text_present('group_ member')
