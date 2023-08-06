__all__ =["StructuredKafkaConsumer", "StructuredKafkaProducer"]

import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "kafka-python-dataclasses"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from .core import from_structure, to_structure
from kafka import KafkaProducer, KafkaConsumer
from functools import partial


StructuredKafkaProducer = partial(
    KafkaProducer,
    value_serializer=from_structure
)

StructuredKafkaConsumer = partial(
    KafkaConsumer,
    value_deserializer=to_structure,
)
