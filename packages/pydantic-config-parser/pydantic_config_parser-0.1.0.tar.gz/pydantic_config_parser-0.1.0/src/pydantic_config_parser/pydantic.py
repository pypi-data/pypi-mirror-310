from pydantic import BaseModel
from pydantic.aliases import AliasChoices
from pydantic.aliases import AliasPath


def get_serialization_key_to_field_key(base_model: BaseModel) -> dict[str, str]:
    serial_to_field_key: dict[str, str] = {}
    for k, field_info in base_model.model_fields.items():
        alias = field_info.validation_alias
        match alias:
            case str():
                serial_to_field_key[alias] = k
            case AliasChoices() as alias_choices:
                for a in alias_choices.choices:
                    match a:
                        case str():
                            serial_to_field_key[a] = k
                        case AliasPath():
                            pass
            case AliasPath() | None:
                serial_to_field_key[k] = k
    return serial_to_field_key
