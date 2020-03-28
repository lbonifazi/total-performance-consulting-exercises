# Total Perform Exercise

## Directory Structure
    .
    ├── data                        # json files directory
    ├── helpers
    |   └── utils.py                # load_json() and get_elements() methods
    ├── logs                        # logs directory
    ├── model                       # models directory
    ├── setup
    |   └── setup_app.py            # constants
    |   └── setup_logger.py         # log configurations
    ├── main_functions.py           # exercise methods
    └── README.md

## Prerequisites
[Python3](https://www.python.org/downloads/) installed

## Usage

This is an test example:
```python
from main_functions import find_element, find_element_near_to

element_a = find_element("Element1")
element_b = find_element_near_to(element_a, "class_name")
if element_b is not None:
    print(element_b.__dict__)
```

## Author

Leonel Bonifazi