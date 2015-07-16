Feature:  Public Views
    A feature that allows the general public to see a few things about the app


Scenario: Signing up
    Given a broswer
    And anyone on the web
    When I go to the signup page
    Then I can create an account
    And I can log in

Scenario: Anonymous View
    Given a browser
    And anyone on the web
    When I visit a group page
    Then I can view that group

Scenario: Create User Profile
    Given a browser
    And anyone on the web
    When I go to the signup page
    Then I can create an account
    Then I will be taken to a create profile page
    And I will create a profile
    And that profile will populate to my page