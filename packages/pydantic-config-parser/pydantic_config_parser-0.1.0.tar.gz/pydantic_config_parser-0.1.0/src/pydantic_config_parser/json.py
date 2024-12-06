import json
import typing as t

from pydantic_config_parser.type import JsonValueType


def json_loads_as_dict(json_s: str | None) -> dict[str, JsonValueType]:
    """utils for type hint"""
    if json_s is None:
        return {}

    v = json.loads(json_s)
    if isinstance(v, dict):
        return t.cast(dict[str, JsonValueType], v)

    err_msg = f"json_s is not dict: {json_s}"
    raise ValueError(err_msg)


def json_loads_as_list(json_s: str | None) -> list[JsonValueType]:
    """utils for type hint"""
    if json_s is None:
        return []

    v = json.loads(json_s)
    if isinstance(v, list):
        return t.cast(list[JsonValueType], v)

    err_msg = f"json_s is not list: {json_s}"
    raise ValueError(err_msg)
