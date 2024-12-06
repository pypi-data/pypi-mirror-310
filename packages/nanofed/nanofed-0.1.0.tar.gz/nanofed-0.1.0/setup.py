# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nanofed',
 'nanofed.cli',
 'nanofed.communication',
 'nanofed.communication.http',
 'nanofed.core',
 'nanofed.data',
 'nanofed.models',
 'nanofed.orchestration',
 'nanofed.server',
 'nanofed.server.aggregator',
 'nanofed.server.model_manager',
 'nanofed.trainer',
 'nanofed.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.10.10,<4.0.0',
 'click>=8.1.7,<9.0.0',
 'numpy>=2.1.2,<3.0.0',
 'pydantic>=2.9.2,<3.0.0',
 'rich>=13.9.4,<14.0.0']

setup_kwargs = {
    'name': 'nanofed',
    'version': '0.1.0',
    'description': 'A lightweight federated learning library',
    'long_description': '# 🚀 NanoFed\n\n**NanoFed**: *Simplifying the development of privacy-preserving distributed ML models.*\n\n---\n\n## 🌍 What is Federated Learning?\n\nFL is a distributed machine learning approach where multiple clients (devices, organizations) collaboratively train a global model without sharing their local data. Instead of sending raw data, clients send model updates to a central server for aggregation. FL enables:\n- **Privacy Preservation**: Data remains on the client device.\n- **Resource Efficiency**: Decentralized training reduces data transfer overload.\n- **Scalable AI**: Collaborative training across distributed environments.\n\n---\n\n## 📦 Installation\n\n**Requires Python 3.10+**\n\n---\n## ⚖️ License\n\nNanoFed is licensed under the GNU General Public License.\n\nMade with ❤️ and 🧠 by [Camille Dunning](https://github.com/camille-004).\n',
    'author': 'camille-004',
    'author_email': 'dunningcamille@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/camille-004/nanofed',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.13',
}


setup(**setup_kwargs)
