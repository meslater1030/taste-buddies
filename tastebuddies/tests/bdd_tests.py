from pytest_bdd import scenario, given, when, then


@scenario('profile.feature', 'Editing User Profile')
def test_edit_user_profile():
    pass


@given('a user')
def user():
    pass


@when('I visit my profile')
def visit_profile():
    pass


@when('I click on the edit profile button')
def edit_profile_button():
    pass


@then('I can edit my profile')
def edit_user_profile():
    pass


@then('profile edits will populate to my page')
def populate_user_profile_edits():
    pass


@scenario('profile.feature', 'Group Suggestions')
def test_group_suggestions():
    pass


@then('I will see suggested groups')
def suggested_groups():
    pass


@scenario('profile.feature', 'Create User Profile')
def test_create_user_profile():
    pass


@when('I first sign up')
def signup():
    pass


@then('I will be taken to a create profile page')
def create_profile_redirect():
    pass


@scenario('profile.feature', 'User Login')
def test_user_login():
    pass


@when('I log in')
def login():
    pass


@then('I will be taken to my profile')
def profile_redirect():
    pass


@scenario('public.feature', 'Signing Up')
def test_signing_up():
    pass


@given('anyone on the web')
def annon():
    pass


@when('I go to the signup page')
def signup_view():
    pass


@then('I can create an account')
def create_account():
    pass


@then('I can log in')
def login_privilege():
    pass


@scenario('public.feature', 'Anonymous View')
def test_anonymous_view():
    pass


@scenario('groups.feature', 'Joining Groups')
def test_joining_groups():
    pass


@when('I visit a group page')
def group_view():
    pass


@then('I can view that group')
def group_view_privilege():
    pass


@then('I can join that group')
def join_group():
    pass


@then('I can see group posts')
def view_group_posts():
    pass


@scenario('groups.feature', 'Leaving Groups')
def test_leaving_groups():
    pass


@given('a group member')
def group_member():
    pass


@then('I can leave that group')
def leave_group():
    pass


@then('I cannot see group posts')
def not_view_group_posts():
    pass


@scenario('groups.feature', 'Create Groups')
def test_create_groups():
    pass


@then('I will see the option to create a group')
def create_group_button():
    pass


@when('I click on the create group button')
def create_group_button_clicked():
    pass


@then('I will be taken to a create group page')
def create_group_redirect():
    pass


@then('that group will be created with my specifications')
def group_creation():
    pass


@then('I will be the admin of that group')
def am_group_admin():
    pass


@scenario('groups.feature', 'Post in Groups')
def test_post_groups():
    pass


@then('I will be able to write a post')
def write_post():
    pass


@then('that post will be visible to other group members')
def post_visible():
    pass


@scenario('groups.feature', 'Delete Group Posts')
def test_delete_group_posts():
    pass


@when('I have created a post')
def create_post():
    pass


@then('I will be able to delete my post')
def delete_my_post():
    pass


@then('that post will not exist')
def post_deleted():
    pass


@scenario('groups.feature', 'View Group Members')
def test_view_group_members():
    pass


@then('I will be able to see all the members of my group')
def see_group_members():
    pass


@scenario('group_admin.feature', 'Admin Delete Posts')
def test_admin_delete_posts():
    pass


@given('a group admin')
def group_admin():
    pass


@when('I visit a group page forum')
def group_forum():
    pass


@then('I will be able to delete any post')
def delete_any_post():
    pass


@scenario('group_admin.feature', 'Admin Delete Group')
def test_admin_delete_group():
    pass


@then('I will be able to delete the group')
def delete_group():
    pass


@then('that group will not exist')
def group_deleted():
    pass


@scenario('group_admin.feature', 'Admin authorization')
def test_admin_authorization():
    pass


@when('I create a group')
def create_group():
    pass


@then('I will have the same authorizations as any group member')
def admin_authorizations():
    pass


@scenario('group_admin.feature', 'Admin Edit Group')
def test_admin_edit_group():
    pass


@then('I will have an edit group button')
def edit_group_button_exists():
    pass


@when('I click the edit group button')
def group_button_clicked():
    pass


@then('I will be able to edit that group')
def edit_group():
    pass


@then('Those edits will be visible to everyone')
def group_edits_populate():
    pass


@scenario('group_admin.feature', 'Admin Delete Group Member')
def test_admin_delete_group_member():
    pass


@then('I will be able to delete a member of the group')
def delete_group_member():
    pass


@then('that user will no longer be a group member')
def group_member_deleted():
    pass
