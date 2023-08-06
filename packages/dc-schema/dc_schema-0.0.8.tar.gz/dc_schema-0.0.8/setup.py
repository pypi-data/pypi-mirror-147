# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dc_schema']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['dc_schema = dc_schema.cli:main']}

setup_kwargs = {
    'name': 'dc-schema',
    'version': '0.0.8',
    'description': 'Generate JSON schema from python dataclasses',
    'long_description': '# dc_schema\n\n[![CI](https://github.com/Peter554/dc_schema/actions/workflows/ci.yaml/badge.svg)](https://github.com/Peter554/dc_schema/actions/workflows/ci.yaml)\n[![codecov](https://codecov.io/gh/Peter554/dc_schema/branch/master/graph/badge.svg?token=YLT3N0HWO9)](https://codecov.io/gh/Peter554/dc_schema)\n\nTiny library to generate [JSON schema](https://json-schema.org/) (2020-12) from python \n[dataclasses](https://docs.python.org/3/library/dataclasses.html). No other dependencies, standard library only.\n\n```\npip install dc-schema \n```\n\n## Assumptions\n\n* python 3.9+ \n\n## Motivation\n\nCreate a lightweight, focused solution to generate JSON schema from plain dataclasses. [pydantic](https://pydantic-docs.helpmanual.io/) is a much more mature option, however it also does a lot of other things I didn\'t want to include here. Deepen my understanding of python dataclasses, typing and JSON schema.\n\n## Usage\n\n### Basics\n\nCreate a regular python dataclass and pass it to `get_schema`.\n\n```py\nimport dataclasses\nimport datetime\nimport json\n\nfrom dc_schema import get_schema\n\n@dataclasses.dataclass\nclass Book:\n    title: str\n    published: bool = False\n\n@dataclasses.dataclass\nclass Author:\n    name: str\n    age: int\n    dob: datetime.date\n    books: list[Book]\n\nprint(json.dumps(get_schema(Author), indent=2))\n```\n\n```json\n{\n  "$schema": "https://json-schema.org/draft/2020-12/schema",\n  "type": "object",\n  "title": "Author",\n  "properties": {\n    "name": {\n      "type": "string"\n    },\n    "age": {\n      "type": "integer"\n    },\n    "dob": {\n      "type": "string",\n      "format": "date"\n    },\n    "books": {\n      "type": "array",\n      "items": {\n        "allOf": [\n          {\n            "$ref": "#/$defs/Book"\n          }\n        ]\n      }\n    }\n  },\n  "required": [\n    "name",\n    "age",\n    "dob",\n    "books"\n  ],\n  "$defs": {\n    "Book": {\n      "type": "object",\n      "title": "Book",\n      "properties": {\n        "title": {\n          "type": "string"\n        },\n        "published": {\n          "type": "boolean",\n          "default": false\n        }\n      },\n      "required": [\n        "title"\n      ]\n    }\n  }\n}\n```\n\n### Annotations\n\nYou can use [typing.Annotated](https://docs.python.org/3/library/typing.html#typing.Annotated) + `SchemaAnnotation` to attach\nmetadata to the schema, such as field descriptions, examples, validation (min/max length, regex pattern, ...), etc. \nConsult [the code](https://github.com/Peter554/dc_schema/blob/master/dc_schema/__init__.py) for full details.\n\n```py\nimport dataclasses\nimport datetime\nimport json\nimport typing as t\n\nfrom dc_schema import get_schema, SchemaAnnotation\n\n@dataclasses.dataclass\nclass Author:\n    name: t.Annotated[str, SchemaAnnotation(title="Full name", description="The authors full name")]\n    age: t.Annotated[int, SchemaAnnotation(minimum=0)]\n    dob: t.Annotated[t.Optional[datetime.date], SchemaAnnotation(examples=["1990-01-17"])] = None\n\nprint(json.dumps(get_schema(Author), indent=2))\n```\n\n```json\n{\n  "$schema": "https://json-schema.org/draft/2020-12/schema",\n  "type": "object",\n  "title": "Author",\n  "properties": {\n    "name": {\n      "type": "string",\n      "title": "Full name",\n      "description": "The authors full name"\n    },\n    "age": {\n      "type": "integer",\n      "minimum": 0\n    },\n    "dob": {\n      "anyOf": [\n        {\n          "type": "string",\n          "format": "date"\n        },\n        {\n          "type": "null"\n        }\n      ],\n      "default": null,\n      "examples": [\n        "1990-01-17"\n      ]\n    }\n  },\n  "required": [\n    "name",\n    "age"\n  ]\n}\n```\n\nTo customize the metadata of a dataclass itself, use a `SchemaConfig`.\n\n```py\nimport dataclasses\nimport json\n\nfrom dc_schema import get_schema, SchemaAnnotation\n\n@dataclasses.dataclass\nclass User:\n    name: str\n\n    class SchemaConfig:\n        annotation = SchemaAnnotation(title="System user", description="A user of the system")\n\nprint(json.dumps(get_schema(User), indent=2))\n```\n\n```json\n{\n  "$schema": "https://json-schema.org/draft/2020-12/schema",\n  "type": "object",\n  "title": "System user",\n  "description": "A user of the system",\n  "properties": {\n    "name": {\n      "type": "string"\n    }\n  },\n  "required": [\n    "name"\n  ]\n}\n```\n\n### Further examples\n\nSee the [tests](https://github.com/Peter554/dc_schema/blob/master/tests/test_dc_schema.py) for full example usage.\n\n## CLI\n\n```\ndc_schema <file_path> <dataclass>\n```\n\ne.g.\n\n```\ndc_schema ./schema.py Author\n```\n\n## Other tools\n\nFor working with dataclasses or JSON schema:\n\n* https://github.com/konradhalas/dacite - create data classes from dictionaries.\n* https://python-jsonschema.readthedocs.io/en/stable/ - validate an object against a JSON schema.\n* https://json-schema.org/understanding-json-schema/index.html - nice reference for understanding JSON schema. \n',
    'author': 'Peter Byfield',
    'author_email': 'byfield554@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Peter554/dc_schema',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
