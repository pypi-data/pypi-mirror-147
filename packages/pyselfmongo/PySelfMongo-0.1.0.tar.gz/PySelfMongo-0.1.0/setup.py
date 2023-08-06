# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyselfmongo']

package_data = \
{'': ['*']}

install_requires = \
['pymongo>=4.1.0,<5.0.0']

setup_kwargs = {
    'name': 'pyselfmongo',
    'version': '0.1.0',
    'description': 'A PySelfMongo client for the [MongoDB][mongo] database is a thin client that connects to a mongo server and provides a simple interface to the database. A client is written as a singleton to make sure that only one connection is open at a time. The connection timeout is taken care by checking the server info every time a request is made. A new connection is made if the server info is not available or the connection has timed out.',
    'long_description': "Py Self Mongo\n==========\n\nA self mongo client for the [MongoDB][mongo] database is a thin client that connects to a mongo server and provides a simple interface to the database.\nA client is written as a singleton to make sure that only one connection is open at a time. The connection timeout is taken care by checking the server info every time a request is made.\nA new connection is made if the server info is not available or the connection has timed out. The project is developed using poetry and the [Pytest][pytest] framework.\n\nHow to use\n----------\n1. Create a config file with name `.mongo_config.yaml` in the root directory of the project. The config file should contain the following fields:\n\n```yaml\nmongo:\n  host:\n    localhost\n  port:\n    27017\n  db_name:\n    db_name\n  password:\n    password\n  username:\n    username\n```\nThe host can be an IP address or a hostname. E.g. In case of a hosted mongo server in aws, the hostname is `ec2-*-**-**-**.**-east-2.compute.amazonaws.com`.\nThe client can be used as follows:\n\n```python\nfrom pyselfmongo import PySelfMongo\n\nmongo_client = PySelfMongo()\nmongo_client.get_collection('collection_name')\n```\n\n2. If no config file is found, the client will try to connect to the localhost with default port 27017. In this case the client can be intialized as follows:\n\n```python\nfrom pyselfmongo import PySelfMongo\n\nmongo_client = PySelfMongo(db_name='db_name', username='user_name', password='password')\nmongo_client.get_collection('collection_name')\n```\n\nMethods and attributes\n---------------------\n- `get_collection(collection_name)`: Returns a collection object.\n- `get_document_by_id(collection_name, document_id)`: Returns a document object.\n- `get_document_by_query(collection_name, query)`: Returns a list of document objects.\n- `get_document_by_query_with_projection(collection_name, query, projection)`: Returns a list of document objects.\n- `get_all_document_generatosr(collection_name, filter)`: Returns a generator of all documents in the collection.\n- `delete_document(collection_name, document_id)`: Deletes a document.\n- `delete_document_by_id(collection_name, document_id)`: Deletes a document.\n- `update_document_by_field(collection_name, field, value)`: Updates a document\n\nInstallation\n------------\nInstall using pip:\n```bash\n$ pip install pyselfmongo\n```\n\n",
    'author': 'Aarif1430',
    'author_email': 'malikarif13@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Aarif1430/PySelfMongo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
