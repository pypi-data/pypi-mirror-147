# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dc_schema']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dc-schema',
    'version': '0.0.3',
    'description': 'Generate JSON schema from python dataclasses',
    'long_description': '# dc_schema\n\nGenerate [JSON schema](https://json-schema.org/) (2020-12) from python \n[dataclasses](https://docs.python.org/3/library/dataclasses.html). No dependencies, standard library only.\n\n```\npip install dc-schema \n```\n\n## Assumptions\n\n* python 3.9+\n* [`from __future__ import annotations`](https://peps.python.org/pep-0563/)\n\n## Usage\n\n### Basics\n\nCreate a regular python dataclass and pass it to `get_schema`.\n\n```py\nfrom __future__ import annotations\n\nimport dataclasses\nimport datetime\nimport json\n\nfrom dc_schema import get_schema\n\n\n@dataclasses.dataclass\nclass Author:\n    name: str\n    age: int\n    dob: datetime.date\n    books: list[Book]\n\n\n@dataclasses.dataclass\nclass Book:\n    title: str\n    published: bool = False\n\n\nprint(json.dumps(get_schema(Author), indent=2))\n```\n\n```\n{\n  "$schema": "https://json-schema.org/draft/2020-12/schema",\n  "type": "object",\n  "title": "Author",\n  "properties": {\n    "name": {\n      "type": "string"\n    },\n    "age": {\n      "type": "integer"\n    },\n    "dob": {\n      "type": "string",\n      "format": "date"\n    },\n    "books": {\n      "type": "array",\n      "items": {\n        "allOf": [\n          {\n            "$ref": "#/$defs/Book"\n          }\n        ]\n      }\n    }\n  },\n  "required": [\n    "name",\n    "age",\n    "dob",\n    "books"\n  ],\n  "$defs": {\n    "Book": {\n      "type": "object",\n      "title": "Book",\n      "properties": {\n        "title": {\n          "type": "string"\n        },\n        "published": {\n          "type": "boolean",\n          "default": false\n        }\n      },\n      "required": [\n        "title"\n      ]\n    }\n  }\n}\n```\n\n### Annotations\n\nYou can use [typing.Annotated](https://docs.python.org/3/library/typing.html#typing.Annotated) + `annotation` to attach\nmetadata to the schema, such as field descriptions, examples, validation (min/max length, regex pattern, ...), etc. \nConsult [the code](https://github.com/Peter554/dc_schema/blob/master/dc_schema/__init__.py) for full details.\n\n```py\nfrom __future__ import annotations\n\nimport dataclasses\nimport datetime\nimport json\nimport typing as t\n\nfrom dc_schema import get_schema, annotation\n\n\n@dataclasses.dataclass\nclass Author:\n    name: t.Annotated[str, annotation(title="Full name", description="The authors full name")]\n    age: t.Annotated[int, annotation(minimum=0)]\n    dob: t.Annotated[t.Optional[datetime.date], annotation(examples=["1990-01-17"])] = None\n\n\nprint(json.dumps(get_schema(Author), indent=2))\n```\n\n```\n{\n  "$schema": "https://json-schema.org/draft/2020-12/schema",\n  "type": "object",\n  "title": "Author",\n  "properties": {\n    "name": {\n      "type": "string",\n      "title": "Full name",\n      "description": "The authors full name"\n    },\n    "age": {\n      "type": "integer",\n      "minimum": 0\n    },\n    "dob": {\n      "anyOf": [\n        {\n          "type": "string",\n          "format": "date"\n        },\n        {\n          "type": "null"\n        }\n      ],\n      "default": null,\n      "examples": [\n        "1990-01-17"\n      ]\n    }\n  },\n  "required": [\n    "name",\n    "age"\n  ]\n}\n```\n\n### Further examples\n\nSee the [tests](https://github.com/Peter554/dc_schema/blob/master/tests/test_dc_schema.py) for full example usage.\n\n\n## Other tools\n\nFor working with dataclasses or JSON schema:\n\n* https://github.com/konradhalas/dacite - create data classes from dictionaries.\n* https://python-jsonschema.readthedocs.io/en/stable/ - validate an object against a JSON schema.\n* https://json-schema.org/understanding-json-schema/index.html - nice reference for understanding JSON schema. ',
    'author': 'Peter Byfield',
    'author_email': 'byfield554@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Peter554/dc_schema',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
