from dataclasses import dataclass

from kafka_dataclasses.core import (
    from_structure,
    to_structure,
    add_class_structure_cache,
)


@dataclass
class Deeper:
    value: float


@dataclass
class Deep:
    value: str
    ruhroh: Deeper


@dataclass
class MyType:
    value: int
    nesting: Deep


def test_from_structure():
    message = MyType(
        value=999,
        nesting=Deep(
            value='inner',
            ruhroh=Deeper(
                value=3.14
            )
        )
    )
    result = from_structure(message)

    assert type(result) is bytes
    assert result == (
        b'{"meta": {"structure_key": "MyType"}, '
        b'"message": {"value": 999, "nesting": {"value": "inner", "ruhroh": {"value": 3.14}}}}'
    )


def test_to_structure():
    the_bytes = (
        b'{"meta": {"structure_key": "MyType"}, '
        b'"message": {"value": 999, "nesting": {"value": "inner", "ruhroh": {"value": 3.14}}}}'
    )

    result = to_structure(the_bytes)

    assert type(result) is dict
    assert result['value'] == 999
    assert result['nesting']['value'] == "inner"


def test_to_structure_with_registered_type():
    the_bytes = (
        b'{"meta": {"structure_key": "MyType"}, '
        b'"message": {"value": 999, "nesting": {"value": "inner", "ruhroh": {"value": 3.14}}}}'
    )

    add_class_structure_cache(
        MyType
    )

    result = to_structure(the_bytes)

    assert type(result) is MyType
    assert result.value == 999
    assert result.nesting.value == "inner"
    assert result.nesting.ruhroh.value == 3.14
