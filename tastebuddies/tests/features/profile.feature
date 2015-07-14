Feature: User Profile
    A feature that allows a user to display their preferences

Scenario: Editing User Profile
    Given a user
    When I click the edit button
    Then I can edit my profile
    And those edits will populate to my page

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