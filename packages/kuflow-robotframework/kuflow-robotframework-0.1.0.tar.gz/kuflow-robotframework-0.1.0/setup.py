# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['KuFlow',
 'kuflow_rest_client',
 'kuflow_rest_client.api',
 'kuflow_rest_client.api.task_api_endpoints',
 'kuflow_rest_client.apis',
 'kuflow_rest_client.model',
 'kuflow_rest_client.models',
 'kuflow_rest_client.test']

package_data = \
{'': ['*'], 'kuflow_rest_client': ['docs/*']}

install_requires = \
['certifi',
 'frozendict==2.3.1',
 'python_dateutil==2.8.2',
 'robotframework==5.0',
 'urllib3==1.26.9']

setup_kwargs = {
    'name': 'kuflow-robotframework',
    'version': '0.1.0',
    'description': 'KuFlow library for Robot Framework',
    'long_description': '<!--[![MIT](https://img.shields.io/github/license/kuflow/kuflow-robotframework?label=License)](https://github.com/kuflow/kuflow-robotframework/blob/master/LICENSE)-->\n<!-- [![Python 3.9+](https://img.shields.io/pypi/pyversions/kuflow-robotframework.svg)](https://pypi.org/project/kuflow-robotframework) -->\n<!-- [![PyPI](https://img.shields.io/pypi/v/kuflow-robotframework.svg)](https://pypi.org/project/kuflow-robotframework) -->\n\n\n# KuFlow Robot Framework\n\nThis library provides keywords to interact with the KuFlow API from a Robot Framework Robot. Its purpose is to facilitate interaction from the robot logic (RPA). Its use helps to keep the manipulation of robot results by Workflow decoupled as much as possible.\n\nList of available keywords:\n\n#### Set Client Authentication\n\n> Configure the client authentication in order to execute keywords against Rest API.\n\n#### Save Element Document \n\n> Save a element task of type document \n\n#### Save Element\n\n> Save a element task\n\n#### Append Log Message\n\n> Add a log entry to the task\n\n\n\n## Documentation\n\nMore detailed docs are available in the [documentation pages](https://docs.kuflow.com/developers/overview/introduction).\n\n\n\n## Contributing\n\nWe are happy to receive your help and comments, together we will dance a wonderful KuFlow. Please review our [contribution guide](CONTRIBUTING.md).\n\n\n\n## License\n\n[MIT License](https://github.com/kuflow/kuflow-robotframework/blob/master/LICENSE)\n',
    'author': 'KuFlow S.L.',
    'author_email': 'kuflow@kuflow.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://kuflow.com/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.11,<4.0.0',
}


setup(**setup_kwargs)
