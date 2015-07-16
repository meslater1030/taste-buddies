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


@given('a browser', scope='module')
def browser():
    browser = Browser()
    return browser


@given('a user', scope="module")
def test_user(browser):
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


@scenario('features/profile.feature', 'Editing User Profile')
def test_edit_user_profile(browser):
    pass


@when('I visit my profile')
def test_visit_profile(browser):
    url = ("http://ec2-52-27-184-229.us-west-2.compute."
           "amazonaws.com/profile/1")
    browser.visit(url)


@when('I click the edit profile button')
def test_edit_profile_button(browser):
    browser.click_link_by_partial_href('/profile/edit')


@then('I can edit my profile')
def test_edit_profile(browser):
    browser.find_by_name('first_name')[0].type('Mary Poppins')
    browser.find_by_name('profile_save')[0].click()


@then('profile edits will populate to my page')
def test_populate_user_profile_edits(browser):
    assert browser.is_text_present('Mary Poppins')


@scenario('features/profile.feature', 'Group Suggestions')
def test_group_suggestions(browser):
    pass


@then('I will see suggested groups')
def test_suggested_groups(browser):
    # update with suggested groups id
    assert browser.find_by_id('suggested_groups')[0].is_text_present('')


@when('I log in')
def test_login(browser):
    pass


@scenario('features/profile.feature', 'User Login')
def test_user_login(browser):
    pass


@then('I will be taken to my profile')
def test_profile_redirect(browser):
    assert browser.url == ('http://ec2-52-27-184-229.us-west-2.compute.'
                           'amazonaws.com/profile/1')


@scenario('features/groups.feature', 'Joining Groups')
def test_joining_groups(browser):
    pass


@when('I visit a group page')
def test_group_view(browser):
    url = ('http://ec2-52-27-184-229.us-west-2'
           '.compute.amazonaws.com/group/1')
    browser.visit(url)


@then('I can join that group')
def test_join_group(browser):
    assert browser.is_element_present_by_name('join')
    browser.find_by_name('join')[0].click()


@then('I can see group posts')
def test_view_group_posts(browser):
    assert browser.is_text_present('forum')


@scenario('features/groups.feature', 'Create Groups')
def test_create_groups(browser):
    pass


@when('I click on the create group button')
def test_create_group_button_clicked(browser):
    browser.find_link_by_partial_href('create_group')[0].click()


@then('I will be taken to a create group page')
def test_create_group_redirect(browser):
    assert browser.url == ('http://ec2-52-27-184-229.us-west-2.compute'
                           '.amazonaws.com/group/create_group')


@then('that group will be created with my specifications')
def test_group_creation(browser):
    browser.find_by_name('group_name')[0].type('Spicy Food Lovers')
    browser.select('age_range', '18-24')
    browser.select('location', 'Eastside')
    browser.find_by_value('Spicy').check
    browser.find_by_value('Barbecue').check
    browser.find_by_value('Mexican').check
    assert browser.find_by_value('Mexican').checked
    browser.choose('group_price', 'cheap')
    browser.find_by_name('profile_save')[0].click()
    assert browser.is_text_present('Spicy Food Lovers')
    assert not browser.is_text_present('Thai')
    assert browser.is_text_present('18-24')
    assert browser.is_text_present('$')


@then('I will be the admin of that group')
def test_am_group_admin(browser):
    assert browser.find_link_by_partial_href('profile_detail')
