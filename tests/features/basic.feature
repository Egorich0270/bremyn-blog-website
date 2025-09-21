Feature: Basic project check
  Scenario: src package is importable
    When I try to import "src"
    Then it should be importable