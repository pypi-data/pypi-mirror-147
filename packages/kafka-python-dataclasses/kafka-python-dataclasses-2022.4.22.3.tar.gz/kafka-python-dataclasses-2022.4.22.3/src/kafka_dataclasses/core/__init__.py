import json
from dataclasses import dataclass
from functools import singledispatch
from logging import Logger

import cattrs
from cattrs.preconf.json import make_converter

from kafka_dataclasses.skeleton import _logger

to_json = make_converter()
ENCODING = ('content-encoding', b'python/dataclass')
default_logger = _logger


@dataclass
class Config:
    logger: Logger
    json_dumps_kwargs: dict
    json_loads_kwargs: dict


_CONFIG = Config(
    logger=default_logger,
    json_dumps_kwargs={},
    json_loads_kwargs={},
)

_CACHE = {}


def get_config():
    return _CONFIG


def configure(config: Config):
    global _CONFIG
    _CONFIG = config


def clear_cache():
    global _CACHE
    _CACHE = {}


def set_structure_cache_for_key(key, the_type: type):
    _CACHE[key] = the_type


@singledispatch
def get_structure_key_for_message(message):
    """
    Return a cache key for the message. This is used to rehydrate messages of this type for
    systems where
    """
    return get_structure_key_for_class(type(message))


def get_structure_key_for_class(klass):
    return klass.__name__


def add_class_structure_cache(klass, key=None):
    if not key:
        key = get_structure_key_for_class(klass)

    set_structure_cache_for_key(key, klass)

    return key


def add_message_to_structure_cache(message, key=None):
    if not key:
        key = get_structure_key_for_message(message)

    return add_class_structure_cache(type(message), key=key)


@dataclass(kw_only=True)
class Meta:
    structure_key: str


@dataclass(kw_only=True)
class StructuredMessage:
    meta: Meta
    message: dict


def from_structure(message) -> bytes:
    structure_key = add_message_to_structure_cache(message)

    envelop = StructuredMessage(
        meta=Meta(
            structure_key=structure_key,
        ),
        message=to_json.unstructure(message),
    )

    return json.dumps(
        to_json.unstructure(envelop),
        **get_config().json_dumps_kwargs,
    ).encode('utf-8')


def to_structure(raw_value: bytes):
    value = json.loads(raw_value.decode('utf-8'), **get_config().json_loads_kwargs)
    structure = to_json.structure(value, StructuredMessage)
    message_class = _CACHE.get(structure.meta.structure_key, False)

    if message_class:
        return cattrs.structure(structure.message, message_class)

    return structure.message
