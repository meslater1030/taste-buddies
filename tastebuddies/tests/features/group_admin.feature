Feature: Admin
    A feature that allows the user who created a group to control it


Scenario: Admin Delete Posts
    Given a group admin
    When I visit a group page forum
    Then I will be able to delete any post
    And that post will not exist

Scenario: Admin Delete Group
    Given a group admin
    When I visit a group page
    Then I will be able to delete the group
    And that group will not exist

Scenario: Admin authorization
    Given a group admin
    When I create a group
    Then I will have the same authorizations as any group member

Scenario: Admin Edit Group
    Given a group admin
    # When I visit a group page
    # Then I will have an edit group button
    When I click the edit group button
    Then I will be able to edit that group
    And Those edits will be visible to everyone

Scenario: Admin Delete Group Member
    Given a group admin
    When I visit a group page
    Then I will be able to delete a member of the group
    And that user will no longer be a group member