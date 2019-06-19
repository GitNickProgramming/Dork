Feature: REPL to facilitate CLI input
  In order to allow for Users to interact with the game
  As a developer
  I want to create a REPL to facilitate action commands

  Scenario: The user starts the game and is prompted
     When the user starts a new game session
     Then the REPL is started
      And a prompt is displayed.

  Scenario: The user inputs a command into the prompt which is evaluated.
     When the user inputs a command
      And the command has a corresponding action.
     Then the command is evaluated and the action is preformed. 

  Scenario: The user inputs a command into the prompt which is evaluated.
     When the user inputs a command
      And the command does not have a corresponding action.
     Then a default command is done

  Scenario: The an action is preformed and the displayed to the user.
     When An action is preformed
      And there is data to display to the user
     Then the data is represented properly to the user.

  Scenario: The an action is preformed that ends the game.
     When An action is preformed
      And the action ends the game
     Then the REPL exits the game.