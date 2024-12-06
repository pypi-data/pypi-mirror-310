# pytrycatch

[![PyPI version](https://badge.fury.io/py/pytrycatch.svg)](https://badge.fury.io/py/pytrycatch)
[![Downloads](https://pepy.tech/badge/pytrycatch)](https://pepy.tech/project/pytrycatch)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

`pytrycatch` is a Python package that simplifies exception handling by providing a decorator to catch exceptions, log them, and return default values. It offers easy customization, including custom error handling functions, logging levels, and exception types.

## Features

- **Automatic error logging**: Logs exceptions automatically when an error occurs.
- **Return safe values**: Allows you to return a safe value (e.g., `None`) when an exception is caught.
- **Custom error handling**: Allows specifying custom functions to handle errors.
- **Flexible logging**: Customizable logging levels.
- **Support for multiple exception types**: You can catch different exception types.

## Installation

You can install [pytrycatch](https://pypi.org/project/pytrycatch/) via [pip](https://pypi.org/):

```bash
pip install pytrycatch
```


## Usage
### Basic Example

```py
from pytrycatch import handle_errors

@handle_errors(log=True, default_return=None)
def test():
    return a + c  # NameError will be raised here

test()
```
### Expected Output:

```sh
ERROR:pytrycatch:Exception in test: name 'a' is not defined
```

## Handling Specific Exceptions
You can specify which exception types you want to handle using the exception_types parameter:

```py
@handle_errors(exception_types=(ZeroDivisionError, ValueError), default_return="Error occurred")
def test():
    return 1 / 0  # ZeroDivisionError will be raised here

result = test()
print(result)  # Output: "Error occurred"
```

## Custom Error Handling
You can define a custom function to handle exceptions:


```py
def custom_error_handler(func, exception):
    print(f"Custom handler for function {func.__name__} caught exception: {exception}")

@handle_errors(log=True, default_return=None, custom_handler=custom_error_handler)
def test():
    return 1 / 0  # ZeroDivisionError will be raised here

result = test()  # This will call custom_error_handler
```

## Custom Logging Levels
The log_level parameter allows you to specify the logging level:

```py
@handle_errors(log=True, default_return=None, log_level=logging.INFO)
def test():
    return 1 / 0  # ZeroDivisionError will be raised here

result = test()  # Logs the error at INFO level instead of ERROR
```


## Multiple Exception Types
You can catch multiple exceptions by passing a tuple of exception types to the exception_types parameter:

```py
@handle_errors(exception_types=(ValueError, ZeroDivisionError), default_return="An error occurred")
def test():
    return int("not a number")  # ValueError will be raised here

result = test()
print(result)  # Output: "An error occurred"
```

## Arguments
* log (bool): Whether to log the exception (default: True).
* default_return (any): The value to return when an exception occurs (default: None).
* exception_types (tuple): A tuple of exception types to catch (default: (Exception,)).
* log_level (int): The logging level to use (default: logging.ERROR).
* custom_handler (function): A custom handler function that takes the function and exception as arguments (default: None).


## Contributing
[Fork](https://github.com/nuhmanpk/pytrycatch/fork) the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature-branch).
Open a pull request.

Made with ❤️ by [Nuhman PK](https://github.com/nuhmanpk)