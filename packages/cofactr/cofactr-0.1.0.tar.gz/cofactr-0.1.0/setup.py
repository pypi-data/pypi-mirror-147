# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cofactr']

package_data = \
{'': ['*']}

install_requires = \
['urllib3>=1.26.9,<2.0.0']

setup_kwargs = {
    'name': 'cofactr',
    'version': '0.1.0',
    'description': 'Client library for accessing Cofactr data.',
    'long_description': '# Cofactr\n\nPython client library for accessing Cofactr.\n\n## Example\n\n```python\nfrom urllib import parse\nfrom cofactr.graph import GraphAPI\n\ngraph_api = GraphAPI()\n\nresistors = graph_api.get_products(\n    query="resistor",\n    fields=["mpn", "assembly"],\n    limit=3,\n    external=False,\n)\n\nmore_resistors = graph_api.get_products(**resistors["paging"]["next"])\n```',
    'author': 'Noah Trueblood',
    'author_email': 'noah@cofactr.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Cofactr/cofactr-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
