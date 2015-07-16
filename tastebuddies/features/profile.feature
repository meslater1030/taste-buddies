Feature: User Profile
    A feature that allows a user to display their preferences

Scenario: Editing User Profile
    Given a browser
    And a user
    When I visit my profile
    And I click the edit profile button
    Then I can edit my profile
    And profile edits will populate to my page

Scenario: Group Suggestions
    Given a browser
    And a user
    When I visit my profile
    Then I will see suggested groups

Scenario: User Login
    Given a browser
    And a user
    When I log in
    Then I will be taken to my profile