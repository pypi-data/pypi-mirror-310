# json parsable types
type JsonValueType = str | int | float | bool | None | list[JsonValueType] | dict[str, JsonValueType]
