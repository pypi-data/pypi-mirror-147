# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['protobuf2arr_tools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'protobuf2arr-tools',
    'version': '0.1.0',
    'description': 'Utility functions and generators for working with the Google protobuf array format.',
    'long_description': '# protobuf2arr-tools\n Utility functions and generators for working with the Google protobuf array format.\n\n## Proto model generator\n\nGenerate a protobuf model from an unknown format protobuf array object. Often times we get protobuf array messages from Google internal services and need to build proto models to interact with them. This tool generates a template for that protobuf array by trying to guess the data type of each index.\n\n### CLI Usage\n```\nusage: proto_builder.py [-h] [--package PACKAGE] arr_json output_proto\n\nBuild a .proto model for an protobuf array.\n\npositional arguments:\n  arr_json           File containing the arr protobuf object.\n  output_proto       File name to save the output .proto model.\n\noptions:\n  -h, --help         show this help message and exit\n  --package PACKAGE  .proto model package name.\n\n```\n\n### Example\n```\n>>> head data.json\n[[null, [[1650289911312855, 44780456, 1997349351], null, 2], 0, "92xdYpeME6iXrcUP58O0uAc"], [[[[["YSF", 0], "Hello World", ... \n\n>>> proto_builder.py data.json message.proto\nGenerated protobuf model: message.proto\n\n>>> head message.proto\nsyntax = "proto3";\n\npackage generated;\n\nmessage EntryPoint {\n\tMsg2 msg1 = 1;\n\tMsg11 msg2 = 2;\n\tstring none3 = 3 [(nullable) = \'\'];\n\tMsg29 msg4 = 4;\n\tstring none5 = 5 [(nullable) = \'\'];\n\tstring none6 = 6 [(nullable) = \'\'];\n\tMsg31Container msg7 = 7;\n\tMsg41 msg8 = 8;\n\tstring none9 = 9 [(nullable) = \'\'];\n\tstring none10 = 10 [(nullable) = \'\'];\n\tstring none11 = 11 [(nullable) = \'\'];\n\tMsg42Container msg12 = 12;\n\tMsg3 msg13 = 13;\n\tstring none14 = 14 [(nullable) = \'\'];\n\tMsg1 msg15 = 15;\n\tstring none16 = 16 [(nullable) = \'\'];\n\tstring none17 = 17 [(nullable) = \'\'];\n\tMsg47 msg18 = 18;\n\tMsg3 msg19 = 19;\n\tstring none20 = 20 [(nullable) = \'\'];\n\tbool field21 = 21;\n}\n\n...\n```',
    'author': 'Kevin Ramdath',
    'author_email': 'krpent@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/minormending/protobuf2arr-tools',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
