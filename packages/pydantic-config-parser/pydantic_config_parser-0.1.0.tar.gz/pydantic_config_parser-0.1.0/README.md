# pydantic-config-parser

This library provides special utility when using pydantic to parse config file.

## Features ✨

- [x] **Override ONLY specified fields** in config file.
- [x] Parse YAML string to JSON object utility.

### Override only specified fields in config file

#### Example 1

```python
from pydantic import BaseModel
from pydantic_config_parser import recursive_override_each_fields

class ConfigRoot(BaseModel):
    a: int = 0
    b: str = "default"

override_json_s = """
{
  "a": 1
}
"""

config = recursive_override_each_fields(ConfigRoot(), json_loads_as_dict(override_json_s))
config.model_dump_json()

# {
#   "a": 1,           # <- override
#   "b": "default"
# }
```

#### Example 2: Override sub model

```python
from pydantic import BaseModel
from pydantic_config_parser import recursive_override_each_fields

class ConfigSub(BaseModel):
    a: int = 0
    b: str = "default"

class ConfigRoot(BaseModel):
    a: int = 0
    b: str = "default"
    c: list[int] = [1, 2, 3]
    d: dict[str, int] = {"a": 1, "b": 2}
    e: ConfigSub = ConfigSub()

override_json_s = """
{
  "e": {
    "a": 2
  }
}
"""

config = recursive_override_each_fields(ConfigRoot(), json_loads_as_dict(override_json_s))
config.model_dump_json()

# {
#   "a": 0,
#   "b": "default",
#   "c": [1, 2, 3],
#   "d": {"a": 1, "b": 2},
#   "e": {
#     "a": 2,             # <- override
#     "b": "default"
#   }
# }
```

### Parse YAML utility

If you want to parse YAML string to JSON object, you can use `yaml_loads_as_dict`.

```sh
pip install pydantic-config-parser[yaml]
```

This will install `PyYAML` as a dependency.

```python
from pydantic_config_parser import yaml_loads_as_json

class ConfigRoot(BaseModel):
    a: int = 0
    b: str = "default"


yaml_s = """
b: test
"""

dict_s = yaml_loads_as_json(yaml_s) # YAML feature is supported

config = recursive_override_each_fields(ConfigRoot(), dict_s)
config.model_dump_json()

# {
#   "a": 0,
#   "b": "test"  # <- override
# }
```
