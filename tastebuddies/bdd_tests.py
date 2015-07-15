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


@scenario('features/groups.feature', 'Leaving Groups')
def test_leaving_groups():
    pass


@given('a group member')
def test_group_member():
    url = ('http://ec2-52-27-184-229.us-west-2'
           '.compute.amazonaws.com/group/1')
    browser.visit(url)


@then('I can leave that group')
def test_leave_group():
    assert browser.is_element_present_by_name('leave')
    browser.find_by_name('leave')[0].click()


@then('I cannot see group posts')
def test_not_view_group_posts():
    assert not browser.is_text_present('forum')


@scenario('features/groups.feature', 'Post in Groups')
def test_post_groups():
    pass


@then('I will be able to write a post')
def test_write_post():
    # this needs to be updated for the name of the post/title?
    browser.find_by_name('post')[0].type('Spicy food is awesome!')


@then('that post will be visible to other group members')
def test_post_visible():
    browser.find_by_name('logout')[0].click()
    browser.find_by_name('login')[0].click()
    browser.find_by_name('username')[0].type('admin2')
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


@scenario('features/groups.feature', 'View Group Members')
def test_view_group_members():
    pass


@then('I will be able to see all the members of my group')
def test_see_group_members():
    # update with group members id or class or whatever
    assert browser.find_by_id('group_members')[0].is_text_present('')


@scenario('features/group_admin.feature', 'Admin Delete Posts')
def test_admin_delete_posts():
    pass


@given('a group admin')
def test_group_admin():
    url = ('http://ec2-52-27-184-229.us-west-2'
           '.compute.amazonaws.com/group/1')
    browser.visit(url)


@when('I visit a group page forum')
def test_group_forum():
    pass


@then('I will be able to delete any post')
def test_delete_any_post():
    # this needs to be updated with the delete button name or id
    browser.find_link_by_partial_href('logout')[0].click()
    browser.find_link_by_partial_href('login')[0].click()
    browser.find_by_name('username')[0].type('admin2')
    browser.find_by_name('password')[0].type('secret')
    browser.find_by_name('submit')[0].click()
    browser.visit('http://ec2-52-27-184-229.us-west-2'
                  '.compute.amazonaws.com/group/1')
    browser.find_by_name('post')[0].type('Spicy food is awesome!')
    browser.find_link_by_partial_href('logout')[0].click()
    browser.find_link_by_partial_href('login')[0].click()
    browser.find_by_name('username')[0].type('admin')
    browser.find_by_name('password')[0].type('secret')
    browser.find_by_name('submit')[0].click()
    browser.visit('http://ec2-52-27-184-229.us-west-2'
                  '.compute.amazonaws.com/group/1')
    browser.find_by_name('delete')[0].click()
    assert not browser.is_text_present('Spicy food is awesome!')


@scenario('features/group_admin.feature', 'Admin Delete Group')
def test_admin_delete_group():
    pass


@then('I will be able to delete the group')
def test_delete_group():
    browser.find_link_by_partial_text('Delete Group')[0].click()


@then('that group will not exist')
def test_group_deleted():
    # Update with test group or else do a test group fixture
    assert browser.is_text_present('Test Group')


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
    assert "\/group\/edit" in browser.url
    browser.find_by_name('group_name')[0].type('Spicy Food Haters')
    browser.find_by_name('profile_save')[0].click()


@then('Those edits will be visible to everyone')
def test_group_edits_populate():
    browser.find_link_by_partial_href('logout')[0].click()
    browser.find_link_by_partial_href('login')[0].click()
    browser.find_by_name('username')[0].type('admin2')
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
    assert not browser.is_text_present('that user')
