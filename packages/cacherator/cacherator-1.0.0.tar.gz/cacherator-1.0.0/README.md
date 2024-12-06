# Cacherator

Cacherator is a Python package that provides decorators to cache class properties and function results in JSON files. This is particularly useful for classes that perform expensive computations or make external API calls, allowing results to persist across program executions.

## Features

- Persistent Caching: Automatically saves and loads class properties and method results to and from JSON files.
- Time-to-Live (TTL) Support: Define how long cached results remain valid.
- Automatic Serialization: Handles JSON serialization of common data types, including datetime objects.
- Customizable Storage: Specify the directory and filename for cached data.
- Logging: Optional logging of cache operations for easier debugging and monitoring.

## Installation

Install the package using pip:
```bash
pip install cacherator
```
## Usage

### Decorating a Class with `json_cache`
Use the `json_cache` decorator to enable caching for a class.

```python
from cacherator import json_cache

@json_cache(ttl=1)
class ExampleClass:
    def __init__(self, example_id="example"):
        self.data_id = example_id

    def expensive_method(self, x):
        # Simulate an expensive computation
        return x ** 2

# Usage
obj = ExampleClass(example_id="example_1")
result = obj.expensive_method(5)  # Calls the method and caches the result
```

When a method from a decorated class object is called again with the same arguments, the cached result will be used as long as the time-to-live of the cache is not exceeded. When the class object is closed (usually when the program ends), the cache will be written to a json file. When the class object is initialized the next time, the stored json will be loaded into the cache.    

### Parameters for json_cache
- `data_id` (str, optional): Unique identifier for the JSON file. Defaults to the class name.
- `directory` (str, optional): Directory where the JSON file will be saved. Defaults to "json/data".
- `clear_cache` (bool, optional): If True, clears any existing cache when initializing the object. Defaults to False.
- `ttl` (float | int | timedelta, optional): Time-to-live for cached function results. Defaults to 999 days.
- `logging` (bool, optional): If True, enables logging of save/load operations. Defaults to True.

Every function in the decorated class automatically accepts two additional named arguments:
- `clear_cache` (bool, optional): If True, clears any existing cache of this function. Defaults to False.
- `ttl` (float | int | timedelta, optional): Set time-to-live for this specific function. Defaults to the class decorator ttl.

## License
This project is licensed under the MIT License.

## Contact
For questions or suggestions, please open an issue on the [GitHub repository](https://github.com/Redundando/json_cache).


