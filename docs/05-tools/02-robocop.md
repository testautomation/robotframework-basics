# 5.2. Robocop

## Goal

* It is always good to have an automated tool to check the syntax of your test code.
* Run `Robocop` to check all your files.

## Solution

!!! info "Hints"
    `Robocop` is a static analysis tool that can be used to check your Robot Framework related files.

    In order to use the `Robocop`, you must first install the `robotframework-robocop` package.

    ``` bash
    pip install robotframework-robocop
    ```

    [Click here to learn more about `Robocop`](https://robocop.readthedocs.io/en/stable/).

## Results

In the `tests` folder, execute the following command.

``` bash
robocop check .
```

You can list all the available rules by executing the following command.

``` bash
robocop list rules
```
