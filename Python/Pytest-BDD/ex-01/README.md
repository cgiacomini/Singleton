# Behavior-Driven-Development (BDD)
***REF***:  
* https://pytest-bdd.readthedocs.io/en/latest/
* https://github.com/AutomationPanda/tau-pytest-bdd
* https://pytest-with-eric.com/bdd/pytest-bdd/

***BDD***  
* Have you ever thought about testing your software behavior from a user’s perspective?
* pytest-bdd is a Pytest plugin that combines the flexibility and power of Pytest with the readability and clarity of BDD.
* Behavior-Driven-Development (BDD) — given a feature, you test its behavior.
* Behavior Driven Development is the practice of software development that puts user behavior at the epicenter of software testing.
***Gerkin***  
* Gherkin is a domain-specific language designed for behavior descriptions, enabling all stakeholders to understand the behavior without needing technical knowledge.
* The syntax is simple, focusing on the use of Given-When-Then statements to describe software features, scenarios, and outcomes.
  
***Pytest BDD Test Framework***   
A BDD framework bridges the features and scenarios specified in your Gherkin feature file and your test code.

## Setup
```
$ python -m venv PyEnv
$ source PyEnv/bin/activate
(PyEnv) $
```
## Simple example 
We start by defining the scenario for testing a specific feature: A deposit into a user account.
```
# tests/features/bank_transactions.feature

Feature: Bank Transactions 
    Tests related to banking Transactions  
  
    Scenario: Deposit into Account  
        Given the account balance is $100  
        When I deposit $20  
        Then the account balance should be $120
```
We now create the test for the scenario
```
# tests/step_definitions/test_bank_transactions.py

import pytest  
from pytest_bdd import scenarios, scenario, given, when, then  
  
# Load all scenarios from the feature file  
scenarios("../features/bank_transactions.feature")  
  
# Fixtures  
@pytest.fixture  
def account_balance():  
    return {"balance": 100}  # Using a dictionary to allow modifications  
  
# Given Steps  
@given("the account balance is $100")  
def account_initial_balance(account_balance):  
    account_balance["balance"] = 100  
  
# When Steps  
@when("I deposit $20")  
def deposit(account_balance):  
    account_balance["balance"] += 20  
  
# Then Steps  
@then("the account balance should be $120")  
def account_balance_should_be(account_balance):  
    assert account_balance["balance"] == 120
```
Run the test
```
$ pytest tests/step_definitions/test_bank_transactions.py -v -s
```
## 2nd simple example (Parameterization Features)
```
# tests/features/bank_transactions_param.feature

Feature: Bank Transactions  
    Tests related to banking Transactions  
  
    Scenario: Deposit into Account  
        Given the account balance is $"100"  
        When I deposit $"20"  
        Then the account balance should be $"120"  
  
    Scenario: Withdraw from Account  
        Given the account balance is $"100"  
        When I withdraw $"20"  
        Then the account balance should be $"80"
```
***Note***: 
1. The numeric values are now in double quotes ("). 
The double-quotes signify that value is a parameter and not to be hardcoded in the tests.
2. We also added a second scenario to test the withdraw from the account.
```
# tests/step_definitions/test_bank_transactions_param.py

import pytest  
from pytest_bdd import scenarios, given, when, then, parsers  
  
# Load all scenarios from the feature file  
scenarios("../features/bank_transactions_param.feature")


# Fixtures  
@pytest.fixture  
def account_balance():  
    return {"balance": 0}  # Using a dictionary to allow modifications  
  
  
# Given Steps  
@given(parsers.parse('the account balance is $"{balance:d}"'))  
def account_initial_balance(account_balance, balance):  
    account_balance["balance"] = balance  
  
  
# When Steps  
@when(parsers.parse('I deposit $"{deposit:d}"'))  
def deposit(account_balance, deposit):  
    account_balance["balance"] += deposit  
  
  
# When Steps  
@when(parsers.parse('I withdraw $"{withdrawal:d}"'))  
def withdraw(account_balance, withdrawal):  
    account_balance["balance"] -= withdrawal  
  
  
# Then Steps  
@then( parsers.parse('the account balance should be $"{new_balance:d}"'),)  
def account_balance_should_be(account_balance, new_balance):  
    assert account_balance["balance"] == new_balance

```
***Note***:
1. parser.parse is used to parse the parameters
2. "{balance:d}” . d just means it’s an int and it’s value is stored as balance


Run the test
```
$ pytest tests/step_definitions/test_bank_transactions_param.py -v -s
```
## 3rd simple example (Scenario Outlines)
Scenario Outlines allows you to specify parameters (called examples) in your feature file.
Similar to Pytest Parametrization it allow to specify a set of input and expected result for the test. 
It is useful when you want to test the same behavior with various inputs and expected outcomes without writing redundant scenarios.

```
# tests/features/bank_transactions_scenario_outline.feature

Feature: Bank Transactions  
    Tests related to banking Transactions  
  
    Scenario Outline: Deposit into Account  
        Given the account balance is $<balance>  
        When I deposit $<deposit>  
        Then the account balance should be $<new_balance>  
        Examples:  
            | balance | deposit | new_balance |  
            | 100     | 20      | 120         |  
            | 0       | 5       | 5           |  
            | 100     | 0       | 100         |
```
***Note***:
<balance>, <deposit>, <new_balance> are fields that take values from the Example table.

```
# tests/step_definitions/test_bank_transactions_scenario_outline.py
import pytest  
from pytest_bdd import scenarios, given, when, then, parsers  
  
# Load all scenarios from the feature file  
scenarios("../features/bank_transactions_scenario_outline.feature")

# Fixture to represent account balance  
@pytest.fixture  
def account_balance():  
    return {"balance": 0}  # Using a dictionary to allow modifications  
 
# Given Steps 
# 1. The string "the account balance is ${balance:d}" is the pattern 
#    to match the step in the feature file
# 2. When the step Given the account balance is $100 is encountered, 
#    100 will be extracted and passed to the step function as the 
#    balance parameter.
# 3. target_fixture="account_balance" : This parameter tells pytest-bdd
#    that the result of this step should be stored in a fixture named 
#    account_balance. 
@given( parsers.parse("the account balance is ${balance:d}"),  
        target_fixture="account_balance",)  
def account_initial_balance(balance):  
    return {"balance": balance}  
  
  
# When Steps  
@when(parsers.parse("I deposit ${deposit:d}"))  
def deposit(account_balance, deposit):  
    account_balance["balance"] += deposit  
  
  
# Then Steps  
@then(parsers.parse("the account balance should be ${new_balance:d}"))  
def account_balance_should_be(account_balance, new_balance):  
    assert account_balance["balance"] == new_balance
````
***Note***:
1. parsers.parse("the account balance is ${balance}") the parser pattern "
1. target_fixture="account_balance"


Run the test
```
$ pytest tests/step_definitions/test_bank_transactions_scenario_outline.py -v -s
```

## 4th simple example (Using Tags)
A typical production project may have hundreds if not thousands of scenarios.
Similar to Pytest markers, you can tag your features and scenarios using the @ symbol.

```
@banking  
Feature: Bank Transactions  
    Tests related to banking Transactions  
  
    @deposit  
    Scenario: Deposit into Account  
        Given the account balance is $"100"  
        When I deposit $"20"  
        Then the account balance should be $"120"  
  
    @withdrawal  
    Scenario: Withdraw from Account  
        Given the account balance is $"100"  
        When I withdraw $"20"  
        Then the account balance should be $"80"
```
Note: 
 * The feature has been tagged with the @banking tag.
 * The scenarios have been tagged as @deposit and @withdraw
 * Tags at Feature level apply to all scenarios level.
Run the Test
```
$ pytest tests -k "deposit"
```
