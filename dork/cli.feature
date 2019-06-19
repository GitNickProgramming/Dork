Feature: User's Command line input of verb/object pairs
  In order to allow for Users to interact with the game
  As a developer
  I want to create accessible actions

  Scenario: The user inputs a valid command and recieves response.
     When the user inputs a command
      And the command contains a defined verb action
      And the command contains a defined object target of the action
     Then the corresponding verb/object command is called.

  Scenario: The user inputs a command missing an object target and recieves help info.
     When the user inputs a command
      And the command contains a defined verb action
      And the command is missing a defined object target of the action
     Then the corresponding verb help info command is called.

  Scenario: The user inputs a unkown command and recieves generic help info
     When the user inputs a command
      And the command is missing a defined verb
     Then the generic help info command is called.