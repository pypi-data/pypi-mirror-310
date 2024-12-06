import json

import yaml
from pydantic import BaseModel
from pydantic import ConfigDict

from pydantic_config_parser.type import JsonValueType


class AnyYaml(BaseModel):
    model_config = ConfigDict(extra="allow")


def yaml_loads_as_json(yaml_s: str) -> JsonValueType:
    """
    yaml で load すると `!!timestamp` 形式の文字列などを `datetime.datetime` など
    に型変換してしまうが、それを行わずに JSON サポートの型として扱うための関数
    例えば `20YY-MM-DDThh:mm:ss` が値に含まれる YAML をロードする時文字列のまま扱いたい場合に使う

    Args:
        yaml_s (str): yaml parsable string

    Returns:
        JsonValueType: JSON support type object
    """
    return json.loads(AnyYaml.model_validate(yaml.safe_load(yaml_s)).model_dump_json())
