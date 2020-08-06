import typing


def merge_obj(
    input: typing.Any, obj: typing.Any, exclude: typing.List[str] = None
) -> typing.Any:
    if not exclude:
        exclude = []
    for attr, value in input.__dict__.items():
        if value is not None and attr not in exclude:
            setattr(obj, attr, value)
    return obj


def merge_dict(
    input: typing.Dict, obj: typing.Any, exclude: typing.List[str] = None
) -> typing.Any:
    if not exclude:
        exclude = []
    for attr, value in input.items():
        if value is not None and attr not in exclude:
            setattr(obj, attr, value)
    return obj
