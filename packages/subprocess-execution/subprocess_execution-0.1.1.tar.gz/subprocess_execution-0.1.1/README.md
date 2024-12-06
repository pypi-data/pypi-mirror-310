# Subprocess Execution

*Efficient tool for running Python code in isolated subprocesses.*

[![PyPI Version](https://img.shields.io/pypi/v/your-library-name.svg)](https://pypi.org/project/your-library-name/)
[![Build Status](https://github.com/joshwadd/subprocess-execution/actions/workflows/ci.yml/badge.svg)](https://github.com/joshwadd/subprocess-execution/actions)
[![License](https://img.shields.io/github/license/joshwadd/subprocess-execution?cacheSeconds=60)](https://github.com/joshwadd/subprocess-execution/blob/main/LICENSE)

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
  - [From PyPI](#from-pypi)
  - [From Source](#from-source)
- [Usage](#usage)
  - [Importing the Decorator](#importing-the-decorator)
  - [Basic Usage](#basic-usage)
  - [Using a Timeout](#using-a-timeout)
  - [Handling Exceptions](#handling-exceptions)
  - [Example](#example)
- [License](#license)
- [Contact](#contact)

---

## Overview

A simple and efficient way to execute arbitrary Python functions in subprocesses, while seamlessly relaying runtime information back to the main process. It is especially useful for diagnosing and resolving system issues that might otherwise crash the Python interpreter.

Designed with minimal dependencies and an intuitive interface, this tool makes it easy to execute any Python callable.


## Installation

### From PyPI

Install the library using `pip`:

```bash
pip install subprocess-execution
```

### From Source

Clone the repository and install:

```bash
git clone https://github.com/joshwadd/subprocess-execution.git
cd subprocess-execution
pip install .
```

## Usage

### Importing the Decorator

First, import the run_in_subprocess decorator from the module:

```python
from subprocess_execution import run_in_subprocess

```

### Basic Usage

Apply the @run_in_subprocess decorator to any function you want to execute in a subprocess:

```python
@run_in_subprocess()
def my_function(arg1, arg2):
    # Function logic here
    return arg1 + arg2
```

Call the function as usual:

```python
result = my_function(5, 10)
print(result)  # Output: 15
```

### Using a Timeout

You can specify a timeout (in seconds) after which the subprocess will be terminated if the function hasn't completed:

```python
@run_in_subprocess(timeout_seconds=300)  # Timeout after 5 minutes
def long_running_function():
    # Potentially long-running operations
    ...
```

### Handling Exceptions
If an exception occurs within the subprocess, it will be raised in the parent process:

```python
@run_in_subprocess()
def faulty_function():
    raise ValueError("An error occurred")

try:
    faulty_function()
except Exception as e:
    print(f"Caught an exception: {e}")
```

### Example

```python
from your_module_name import run_in_subprocess

@run_in_subprocess(timeout_seconds=10)
def compute_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

if __name__ == "__main__":
    numbers = list(range(1000000))
    try:
        result = compute_sum(numbers)
        print(f"The sum is: {result}")
    except Exception as e:
        print(f"An error occurred: {e}")

```

## License

This project is licensed under the MIT License.


## Contact

For questions or feedback, feel free to reach out:

Email: josh.waddington1@gmail.com









