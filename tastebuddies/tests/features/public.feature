Feature:  Public Views
    A feature that allows the general public to see a few things about the app


Scenario: Signing up
    Given anyone on the web
    When I go to the signup page
    Then I can create an account
    And I will be able to log in

Scenario: Anonymous View
    Given anyone on the web
    When I visit a group page
    Then I can view that group