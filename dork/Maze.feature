Feature: Random Maze Generation 
  In order to allow for Users to have interesting games
  As a developer
  I want to create a system for the game to create Mazes programmatically

  Scenario: The an user starts a new game without map data to generate a new maze.
     When An the user starts a new game
      And there is no map data provided by the user
     Then the game generates a new map/maze.
      And the map is (maybe fully) connected.

Feature: Loaded Maze Generation 
  In order to allow for Users to have progress in games
  As a developer
  I want to create a system for the game to load Mazes provided by the user

  Scenario: The an user starts a new game with map data to load into the game.
     When An the user starts a new game
      And there is map data provided by the user
     Then the game loads the map/maze.
      And the map is checked for completeness and connectivity.
