Feature: Groups
    A feature that allows a user to connect with other users with similar food preferences

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