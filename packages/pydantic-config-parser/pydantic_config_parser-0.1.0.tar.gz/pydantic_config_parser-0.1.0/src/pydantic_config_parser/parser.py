import json
import typing as t
from logging import NullHandler
from logging import getLogger

from pydantic import BaseModel

from pydantic_config_parser.pydantic import get_serialization_key_to_field_key
from pydantic_config_parser.type import JsonValueType

LOGGER = getLogger(__name__)
LOGGER.addHandler(NullHandler())

BaseModelT = t.TypeVar("BaseModelT", bound=BaseModel)


def recursive_override_each_fields(base_model: BaseModelT, override_mapping: dict[str, JsonValueType]) -> BaseModelT:
    """
    BaseModel に対して再帰的に上書きを行う。
    dict に関しては各 field 事に上書きを行うがlist 型に対しては list ごと上書きを行うので注意。
    # alias の場合を考慮するため json.dumps / json.loads を利用する場面がある

    Args:
        base_model (BaseModel): 上書きされる BaseModel
        override_mapping (dict[str, JsonValueType]):
            上書きする値。
            `base_model` 側で alias を指定している場合、 override_mapping は alias 前の key である必要がある。
    """
    alias_to_key: dict[str, str] = get_serialization_key_to_field_key(base_model)

    # BaseModel を dict で上書きするため、一度 BaseModel を dict に変換して対応を見ていく
    new_dict: dict[str, JsonValueType] = json.loads(base_model.model_dump_json(by_alias=True))
    for override_key, override_val in override_mapping.items():
        field_key = alias_to_key[override_key]
        field_val: JsonValueType | BaseModel
        match (field_val := getattr(base_model, field_key), override_val):
            case BaseModel(), dict():
                if set(override_val.keys()).issubset(
                    get_serialization_key_to_field_key(field_val).keys()
                ):  # 同じ field を持つ場合は同じ型と考えて各fieldごとに上書き
                    new_dict[override_key] = json.loads(
                        recursive_override_each_fields(base_model=field_val, override_mapping=override_val).model_dump_json(by_alias=True)
                    )
                else:  # field が異なる場合は完全に入れ替える
                    new_dict[override_key] = override_val
            case (
                (_, None)  # nullable な field であれば None で上書き
                | (BaseModel(), _)
                | (list(), list())  # list の場合は list 全体を上書き
                | (dict(), dict())  # dict field は完全に上書き
                | (None, _)  # 元が None の場合は上書き。 nullable な型ではない場合は validate 時にエラー
                | (_, _)  # 型が annotation と違う場合は validate 時にエラーになる
            ):
                new_dict[override_key] = override_val  # そのまま上書き。型が違う場合は validate 時にエラーになる
    return base_model.__class__.model_validate_json(json.dumps(new_dict))


T = t.TypeVar("T")


def recursive_override_helper(*, field_types: tuple[type[T], ...], override_v: JsonValueType) -> JsonValueType:
    LOGGER.debug(f"field_types: {tuple(field_types)}, value: {override_v}, origin: {t.get_origin(tuple(field_types))}")
    f_type: type[T]
    for f_type in field_types:
        LOGGER.debug(f"field_type: {f_type}, value: {override_v}")
        match f_type:
            case _type if t.get_origin(_type) is t.Annotated:  # typing.Annotated[SomeClass, Strict()] の場合は剥がす
                return recursive_override_helper(field_types=(t.get_args(_type)[0],), override_v=override_v)
            case _type if issubclass(_type, BaseModel):
                match override_v:
                    case dict():
                        json_s = json.dumps(override_v)
                        try:
                            _type.model_validate_json(json_s)  # validate に成功すれば良い
                        except Exception as e:
                            LOGGER.debug(f"{_type} model_validate failed: {e}")
                            continue  # 次に field を試す
                        return override_v
                    case _:
                        err_msg = f"field `{f_type}` in the overriding map is not a dict, but `{type(override_v)}: {override_v}`"
                        LOGGER.error(err_msg)
                        raise TypeError(err_msg)
            case _type if t.get_origin(_type) is list:
                match override_v:
                    case list():
                        return [recursive_override_helper(field_types=t.get_args(_type), override_v=v) for v in override_v]
                    case _:
                        LOGGER.debug(f"list type is not matched: {override_v}")
                        continue
            case _:  # int | str | float | bool | None | dict
                LOGGER.debug(f"simple value: {override_v}")
                return override_v
    err_msg = f"value `{override_v}` is not matched with field_types `{field_types}`"
    raise TypeError(err_msg)
