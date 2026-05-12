# A.1. Variables

This page summarizes how variables work in Robot Framework, including the different types, how to declare them, available scopes, type conversion, and useful information.

## Variable types

There are three types of Robot Framework variables, distinguished by their prefix character:

| Prefix | Type                       | Example declaration |
|--------|----------------------------|---------------------|
| `$`    | Scalar (any Python object) | `${name}`           |
| `@`    | List                       | `@{names}`          |
| `&`    | Dictionary                 | `&{stock}`          |

A scalar can hold any type of Python value, including strings, numbers, lists, dictionaries, and any object returned by a keyword. The `@{...}` and `&{...}` prefixes mainly matter when *declaring* a list or dictionary, or when expanding one into multiple arguments at a call site.

## Declaring variables

### In the `*** Variables ***` section

Declares variables at the suite scope, making them available to every test case in the suite file:

``` robotframework
*** Variables ***
${NAME}      Jane Doe
${COUNT}     ${4}
@{NAMES}     Jane Doe    John Doe
&{STOCK}     idared=${4}    jonagold=${3}
```

### With the `VAR` keyword

`VAR` creates variables at runtime with a configurable scope. The default scope is `LOCAL`:

``` robotframework
*** Test Cases ***
Create Variables
    VAR    ${apple}     idared
    VAR    ${count}     ${4}
    VAR    @{apples}    idared    jonagold
    VAR    &{stock}     idared=${4}    jonagold=${3}
```

### Assignment from a keyword

A variable can capture the return value of a keyword:

``` robotframework
${result}=    Catenate    Hello    World
```

### From the command line

Use the `--variable` option to pass values into a test run:

``` bash
robot --variable NAME:JaneDoe tests/
```

### Environment variables

Use the `%{NAME}` syntax to read a process environment variable:

``` robotframework
Log To Console    %{TOKEN}
```

## Variable scopes

`VAR` accepts an explicit `scope` argument:

| Scope    | Visibility                                           |
|----------|------------------------------------------------------|
| `LOCAL`  | Current keyword or test case (default)               |
| `TEST`   | Current test case (alias: `TASK` when running tasks) |
| `SUITE`  | Current suite                                        |
| `SUITES` | Current suite **and its child suites**               |
| `GLOBAL` | Everywhere - every suite and every test in the run   |

``` robotframework
VAR    ${config}    something    scope=GLOBAL
```

!!! note
    The `*** Variables ***` section is roughly equivalent to declaring variables with `scope=SUITE`. The older `Set Local Variable`, `Set Test Variable`, `Set Suite Variable`, and `Set Global Variable` keywords are equivalents of `VAR` with the corresponding scope.

## Strings vs. Python values

By default, a literal value in `VAR` is a **string**:

``` robotframework
VAR    ${count}    4        # ${count} is the string "4"
```

Use the `${...}` syntax to write a **Python value**:

``` robotframework
VAR    ${count}    ${4}     # ${count} is the integer 4
```

You can verify a variable's Python type with the inline `${{ ... }}` evaluator:

``` robotframework
Log To Console    ${{ type($count) }}
```

The `${{ ... }}` form evaluates an arbitrary Python expression. Use `$name` (no braces) inside it to reference a variable.

## Variable type conversion

Starting with version 7, Robot Framework supports declaring the target type of a variable with a `: type` suffix. The value is parsed or converted to the declared Python type at assignment time.

### Built-in types

``` robotframework
VAR    ${count: int}      4         # int(4)
VAR    ${ratio: float}    4.7       # float(4.7)
VAR    ${active: bool}    True      # True
```

### Union types

``` robotframework
VAR    ${count: int | float}    4.7    # float(4.7)
```

### Lists and dictionaries

``` robotframework
VAR    @{numbers: int}              1    2    3    4
VAR    ${numbers: list[int]}        [1, 2, 3, 4]
VAR    &{stock: int}                idared=4    jonagold=3
VAR    &{stock: str=int}            idared=4    jonagold=3
VAR    ${stock: dict[str, int]}     {"idared": 4, "jonagold": 3}
```

The `${name: list[...]}` and `${name: dict[...]}` forms accept a single string and parse it. The `@{name: ...}` and `&{name: ...}` forms apply the type to each element.

Type annotations also work on keyword assignments:

``` robotframework
${count: int}=    Get Count From Somewhere
```

A conversion failure occurs immediately upon declaration:

``` robotframework
VAR    ${count: int}    abc    # immediate conversion error
```

## Dictionary access

Dictionaries that are declared using the `&{...}` syntax support two access styles:

``` robotframework
${stock.idared}      # dot access (DotDict)
${stock["idared"]}   # bracket access
```

Dot access works because Robot Framework wraps these dictionaries in a `DotDict`. However, dictionaries created with `${name: dict}` (or `${name: dict[...]}`), as well as plain Python dictionaries returned from libraries, are regular Python dictionary objects and do **not** support dot access. Use bracket notation for these instead.

## Secrets

`Secret` (available since Robot Framework 7.4) is a type that masks the value in logs, console output, and reports:

``` robotframework
VAR    ${token: Secret}    %{TOKEN}
Log To Console    ${token}    # prints <secret>
```

The `VAR    ${name: Secret}    ...` form is restricted: the value must come from an environment variable (`%{NAME}`), or from a variable that is already a `Secret`. Inline literals, command-line variables passed with the `--variable` flag, and references to non-`Secret` variables all fail with `Value must have type 'Secret', got <type>`, where `<type>` is the actual type of the supplied value (`string`, `integer`, `list`, `dictionary`, `None`, etc.). This prevents secrets from being hardcoded into the source.

In a Python library, return `Secret` instances when a value should not appear in logs:

``` python
from robot.api.types import Secret


def generate_secure_password():
    return Secret("my-password")
```

The `: Secret` annotation can also be used on keyword assignments. In this position, it *validates* that the keyword returns a `Secret` - it does not coerce a plain string. The example below only works because `Generate Secure Password` returns a `Secret` object:

``` robotframework
${password: Secret}=    Generate Secure Password
```

If the keyword returned a value of any other type, the assignment would fail with `ValueError: Return value must have type 'Secret', got <type>.`

### Older alternative: `Set Log Level`

Before `Secret`, one way to prevent sensitive information from being included in the generated artifacts was to temporarily lower the log level:

``` robotframework
Set Log Level    NONE
Log    %{TOKEN}
Set Log Level    TRACE
```

This hides the value from the generated artifacts (`log.html`, `output.xml`, `report.html`). The log level has no effect on `Log To Console`, which always writes to standard output. This technique is also much coarser than `Secret` as it suppresses *all* log messages within its range, not just the sensitive value. **Prefer `Secret` whenever possible**, as it limits the masking to the specific variable rather than the entire log stream.

## Built-in variables

Robot Framework provides several variables out of the box:

| Variable                         | Value                                                               |
|----------------------------------|---------------------------------------------------------------------|
| `${True}`, `${False}`, `${None}` | Python literals                                                     |
| `${EMPTY}`                       | empty string                                                        |
| `${SPACE}`                       | a single space                                                      |
| `${\n}`                          | newline                                                             |
| `${/}`                           | OS-specific path separator                                          |
| `${CURDIR}`                      | absolute path to the current suite directory                        |
| `${EXECDIR}`                     | absolute path to the directory where the test execution was started |
| `${TEMPDIR}`                     | system temp directory                                               |

[Click here to see the full list of built-in variables](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#built-in-variables).

## Things to be aware of

- **Strings by default**: A literal `4` is the string `"4"`, not the integer `4`. Use the `${4}` syntax or the `: int` type annotation to get an integer.
- **`VAR` defaults to `LOCAL` scope**: A `VAR` inside a keyword does not propagate to the calling test unless you pass `scope=TEST`, `scope=SUITE`, or higher.
- **Dot access is only available for `DotDict`**: Only dictionaries declared with `&{...}` are wrapped in a `DotDict` and support dot access. This does not apply to dictionaries created with `${name: dict}` (or `${name: dict[...]}`), nor to plain Python dictionaries returned from libraries.
- **Type conversion fails early**: `VAR    ${count: int}    abc` fails at declaration, before the variable is bound.
- **`SUITES` is `SUITE` with children**: `SUITES` makes the variable visible to the current suite **and** all its descendant suites, whereas `SUITE` is limited to the current suite only.

---

[Click here to learn more about variables in the Robot Framework User Guide](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#variables).
