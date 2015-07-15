Feature: Groups
    A feature that allows a user to connect with other users with similar food preferences

Scenario: Joining Groups
    Given a user
    When I visit a group page
    Then I can join that group
    And I can see group posts

Scenario: Leaving Groups
    Given a group member
    When I visit a group page
    Then I can leave that group
    And I cannot see group posts


Scenario: Create Groups
    Given a user
    When I click on the create group button
    Then I will be taken to a create group page
    And that group will be created with my specifications
    And I will be the admin of that group

Scenario: Post in Groups
    Given a group member
    When I visit a group page
    Then I will be able to write a post
    And that post will be visible to other group members

Scenario: Delete Group Posts
    Given a group member
    When I have created a post
    Then I will be able to delete my post
    And that post will not exist


Scenario: View Group Members
    Given a group member
    When I visit a group page
    Then I will be able to see all the members of my group