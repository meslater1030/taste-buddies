# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pytest_bdd import scenario, given, when, then
from cryptacular.bcrypt import BCRYPTPasswordManager
import models
import os
from pyramid import testing

os.environ['TESTING'] = "True"


@scenario('features/profile.feature', 'Editing User Profile')
def test_edit_user_profile():
    pass


@given('a user')
def test_user(request):
    manager = BCRYPTPasswordManager()
    settings = {
        'auth.username': 'admin',
        'auth.password': manager.encode('secret'),
    }
    testing.setUp(settings=settings)
    req = testing.DummyRequest()

    def cleanup():
        testing.tearDown()

    request.addfinalizer(cleanup)

    return req


@when('I visit my profile')
def test_visit_profile():
    pass


@when('I click the edit profile button')
def test_edit_profile_button():
    pass


@then('I can edit my profile')
def test_edit_profile():
    pass


@then('profile edits will populate to my page')
def test_populate_user_profile_edits():
    pass


@scenario('features/profile.feature', 'Group Suggestions')
def test_group_suggestions():
    pass


@then('I will see suggested groups')
def test_suggested_groups():
    pass


@scenario('features/profile.feature', 'Create User Profile')
def test_create_user_profile():
    pass


@when('I first sign up')
def test_signup():
    pass


@then('I will be taken to a create profile page')
def test_create_profile_redirect():
    pass


@scenario('features/profile.feature', 'User Login')
def test_user_login():
    pass


@when('I log in')
def test_login():
    pass


@then('I will be taken to my profile')
def test_profile_redirect():
    pass


@scenario('features/public.feature', 'Signing up')
def test_signing_up():
    pass


@given('anyone on the web')
def test_annon():
    pass


@when('I go to the signup page')
def test_signup_view():
    pass


@then('I can create an account')
def test_create_account():
    pass


@then('I can log in')
def test_login_privilege():
    pass


@scenario('features/public.feature', 'Anonymous View')
def test_anonymous_view():
    pass


@scenario('features/groups.feature', 'Joining Groups')
def test_joining_groups():
    pass


@when('I visit a group page')
def test_group_view():
    pass


@then('I can view that group')
def test_group_view_privilege():
    pass


@then('I can join that group')
def test_join_group():
    pass


@then('I can see group posts')
def test_view_group_posts():
    pass


@scenario('features/groups.feature', 'Leaving Groups')
def test_leaving_groups():
    pass


@given('a group member')
def test_group_member():
    pass


@then('I can leave that group')
def test_leave_group():
    pass


@then('I cannot see group posts')
def test_not_view_group_posts():
    pass


@scenario('features/groups.feature', 'Create Groups')
def test_create_groups():
    pass


@when('I click on the create group button')
def test_create_group_button_clicked():
    pass


@then('I will be taken to a create group page')
def test_create_group_redirect():
    pass


@then('that group will be created with my specifications')
def test_group_creation():
    pass


@then('I will be the admin of that group')
def test_am_group_admin():
    pass


@scenario('features/groups.feature', 'Post in Groups')
def test_post_groups():
    pass


@then('I will be able to write a post')
def test_write_post():
    pass


@then('that post will be visible to other group members')
def test_post_visible():
    pass


@scenario('features/groups.feature', 'Delete Group Posts')
def test_delete_group_posts():
    pass


@when('I have created a post')
def test_create_post():
    pass


@then('I will be able to delete my post')
def test_delete_my_post():
    pass


@then('that post will not exist')
def test_post_deleted():
    pass


@scenario('features/groups.feature', 'View Group Members')
def test_view_group_members():
    pass


@then('I will be able to see all the members of my group')
def test_see_group_members():
    pass


@scenario('features/group_admin.feature', 'Admin Delete Posts')
def test_admin_delete_posts():
    pass


@given('a group admin')
def test_group_admin():
    pass


@when('I visit a group page forum')
def test_group_forum():
    pass


@then('I will be able to delete any post')
def test_delete_any_post():
    pass


@scenario('features/group_admin.feature', 'Admin Delete Group')
def test_admin_delete_group():
    pass


@then('I will be able to delete the group')
def test_delete_group():
    # write a function to click the delete button
    pass


@then('that group will not exist')
def test_group_deleted():
    # query the database for the group and assert false
    pass


@scenario('features/group_admin.feature', 'Admin authorization')
def test_admin_authorization():
    pass


@when('I create a group')
def test_create_group():
    # go to group creation page and input data
    pass


@then('I will have the same authorizations as any group member')
def test_admin_authorizations():
    # is this really necessary?  Is there a way to compare authorizations?
    pass


@scenario('features/group_admin.feature', 'Admin Edit Group')
def test_admin_edit_group():
    pass


@when('I click the edit group button')
def test_group_button_clicked():
    # ?? Some action that clicks the button for us.  webtest?
    pass


@then('I will be able to edit that group')
def test_edit_group():
    # we want to check to see whether the user is redirected to
    # an edit group page that will accept input.
    pass


@then('Those edits will be visible to everyone')
def test_group_edits_populate():
    # we pull the html/beautiful soup for the page and check to be
    # sure that our edits are shown there.
    pass


@scenario('features/group_admin.feature', 'Admin Delete Group Member')
def test_admin_delete_group_member():
    pass


@then('I will be able to delete a member of the group')
def test_delete_group_member():
    # there needs to be a delete option only visible to the admin
    # clicking on that delete button grabs the id for that user
    # we user that user id to delete the user from the group table
    pass


@then('that user will no longer be a group member')
def test_group_member_deleted():
    # assert the group user is not in a query of the users located in the
    # table for that group
    pass