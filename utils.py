import json
from typing import Union, Callable, Any

import rx
from rx.operators import map, map_indexed


def after(action: Callable[[Any], None]) -> Callable[[Any], Any]:
    def do_before(value: any) -> any:
        action(value)
        return value

    return do_before


def do(action: Callable[[Any], None]):
    return rx.pipe(
        map(after(action))
    )


def component(index: int):
    return rx.pipe(
        map(lambda pair: pair[index])
    )


def indexed():
    return rx.pipe(
        map_indexed(lambda i, idx: (i, idx))
    )


Json = Union[list, dict, str, int, bool, float]


def load_json(path: str) -> Json:
    with open(path, 'r') as load_file:
        return json.load(load_file)


def format_json(data: Json) -> str:
    return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


def save_json(data: Json, path: str):
    with open(path, 'w') as save_file:
        save_file.write(format_json(data))
