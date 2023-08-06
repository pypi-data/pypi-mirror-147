.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

================================
kafka-python-dataclasses
================================


    Structured messages for your kafka projects


Kafka is a really complex library and dealing with bytes can be taxing. Use these
wonderful structured Kafka classes instead!

Basic consuming:

.. code-block:: python

   from dataclasses import dataclass
   from kafka_dataclasses import StructuredKafkaConsumer


   @dataclass
   class MyKafkaMessage:
      value: str


   for message in StructuredKafkaConsumer(['my_topic']):
      assert type(message) == MyKafkaMessage


Basic producing:

.. code-block:: python

   from dataclasses import dataclass
   from kafka_dataclasses import StructuredKafkaProducer


   @dataclass
   class MyKafkaMessage:
      value: str


   StructuredKafkaProducer().send('my_topic', MyKafkaMessage("Hello, world!"))

This works on deeply nested dataclasses as well!
In theory it will also work on attrs classes, since the
unstructuring library, `cattrs`, supports `attrs` out of the box.


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.2.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
