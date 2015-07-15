Feature: Signup
    A feature that allows you to become a user

Scenario: Signing up
    Given an anonymous user
    When I go to the signup page
    Then I can create an account
    And I will be able to log in

Scenario: Anonymous View
    Given an anonymous user
    When I visit a group page
    Then I can view that group

Scenario: Editing User Profile
    Given a user
    When I click the edit button
    Then I can edit my profile
    And those edits will populate to my page

Scenario: Joining Groups
    Given a user
    When I visit the page for a group
    Then I can join that group
    And I will be able to see posts

Scenario: Leaving Groups
    Given a group member
    When I visit the page for a group
    Then I can leave that group
    And I will no longer be able to see posts

Scenario: Group Suggestions
    Given a user
    When I visit my profile
    Then I will see suggested groups

Scenario: Create User Profile
    Given a user
    When I first sign up
    Then I will be taken to a create profile page
    And those edits will populate to my page

Scenario: User Login
    Given a user
    When I log in
    Then I will be taken to my profile

Scenario: Create Groups
    Given a user
    When I visit my profile
    Then I will see the option to create a group
    When I click on that option
    Then I will be take to a create group page
    And that group will be created with my specifications
    And I will become the admin of that group

Scenario: Post in Groups
    Given a group member
    When I visit my group page
    Then I will be able to write a post
    And that post will be visible to other group members

Scenario: Delete Group Posts
    Given a group member
    When I have created a post
    Then I will be able to delete that post
    And that post will not be visible to anyone

Scenario: View Group Members
    Given a group member
    When I visit the group page
    Then I will be able to see all the members of that group

Scenario:
    Given a group admin
    When I visit the group page forum
    Then I will be able to delete any post
    And that post will not be visible to anyone

Scenario:
    Given a group admin
    When I visit the group page
    Then I will be able to delete the group
    And that group will no longer exist

Scenario:
    Given a group admin
    When I create a group
    Then I will have the same authorizations as any group member

Scenario:
    Given a group admin
    When I visit the group page
    Then I will have an edit button
    When I click the edit button
    Then I will be able to edit that group
    And Those edits will be visible to everyone

Scenario:
    Given a group admin
    When I visit the group page
    Then I will be able to delete a member of the group
    And that user will no longer be a group member