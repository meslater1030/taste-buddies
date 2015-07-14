from pytest_bdd import scenario, given, when, then


@scenario('profile.feature', 'Editing User Profile')
def test_edit_user_profile():
    pass


@scenario('profile.feature', 'Group Suggestions')
def test_group_suggestions():
    pass


@scenario('profile.feature', 'Create User Profile')
def test_create_user_profile():
    pass


@scenario('profile.feature', 'User Login')
def test_user_login():
    pass


@scenario('public.feature', 'Signing Up')
def test_signing_up():
    pass


@scenario('public.feature', 'Anonymous View')
def test_anonymous_view():
    pass


@scenario('groups.feature', 'Joining Groups')
def test_joining_groups():
    pass


@scenario('groups.feature', 'Leaving Groups')
def test_leaving_groups():
    pass


@scenario('groups.feature', 'Create Groups')
def test_create_groups():
    pass


@scenario('groups.feature', 'Post in Groups')
def test_post_groups():
    pass


@scenario('groups.feature', 'Delete Group Posts')
def test_delete_group_posts():
    pass


@scenario('groups.feature', 'View Group Members')
def test_view_group_members():
    pass


@scenario('group_admin.feature', 'Admin Delete Posts')
def test_admin_delete_posts():
    pass


@scenario('group_admin.feature', 'Admin Delete Group')
def test_admin_delete_group():
    pass


@scenario('group_admin.feature', 'Admin authorization')
def test_admin_authorization():
    pass


@scenario('group_admin.feature', 'Admin Edit Group')
def test_admin_edit_group():
    pass


@scenario('group_admin.feature', 'Admin Delete Group Member')
def test_admin_delete_group_member():
    pass
