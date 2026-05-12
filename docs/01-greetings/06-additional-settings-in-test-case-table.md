# 1.6. Additional settings in Test Case table

## Goal

* Tag one of your test cases with `ubuntu` and tag the other one with `centos`.
* Write brief documentation for both test cases.
* Make the `Greetings Again` test case log a message before it starts and another message after it finishes.

## Solution

!!! info "Hints"
    You can tag test cases using the `[Tags]` setting in Test Case table.

    You can write documentation using the `[Documentation]` setting in Test Case table.

    You can define test-level setups and teardowns using the `[Setup]` and `[Teardown]` settings in Test Case table. These settings run before and after each test case. In contrast, the Suite Setup and Suite Teardown settings, which are covered in the next chapter, run once per suite.

    [Click here to learn more about the available settings in Test Case table](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#test-case-section).

    [Click here to learn more about test setup and teardown](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#test-setup-and-teardown).

??? success "Solution: `tests/01-greetings/01-greetings.robot`"
    ``` robotframework hl_lines="11 12 17 18 19 21"
    *** Settings ***
    Resource    ${CURDIR}${/}resources${/}greetings.resource


    *** Variables ***
    ${YOUR_NAME}    Your Name


    *** Test Cases ***
    Original Greetings
        [Documentation]    This test case verifies that the Print Your Name keyword works as expected.
        [Tags]    ubuntu
        Print Your Name
        Print Your Name    ${YOUR_NAME}

    Greetings Again
        [Documentation]    This test case proves that we can import variables from resource files.
        [Tags]    centos
        [Setup]    Log    Test setup for "Greetings Again" test case.
        Print Your Name    ${ANOTHER_NAME_IN_RESOURCE}
        [Teardown]    Log    Test teardown for "Greetings Again" test case.
    ```

## Results

In the `tests` folder, execute the following command.

``` bash
robot .
```

You can use the `--include` parameter to select test cases by a tag.
``` bash
robot --include centos .
robot --include ubuntu .
```

You can check the generated `log.html` file to see how your test cases worked.
