# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydastic']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch>=7.12.0,<8.0.0', 'pydantic>=1.9.0,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=4.5.0,<5.0.0']}

setup_kwargs = {
    'name': 'pydastic',
    'version': '0.2.2',
    'description': 'Pydastic is an elasticsearch python ORM based on Pydantic.',
    'long_description': '<div align="center">\n\n<img src="https://github.com/RamiAwar/pydastic/raw/main/assets/images/pydastic.png" width="200" height="200" />\n<h1>Pydastic</h1>\n\n<a href="https://pypi.org/project/pydastic" target="_blank">\n    <img src="https://img.shields.io/pypi/v/pydastic?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n\n[![build](https://github.com/RamiAwar/pydastic/actions/workflows/build.yml/badge.svg)](https://github.com/RamiAwar/pydastic/actions/workflows/build.yml)\n[![Python Version](https://img.shields.io/pypi/pyversions/pydastic.svg)](https://pypi.org/project/pydastic/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/ramiawar/pydastic/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/ramiawar/pydastic/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/ramiawar/pydastic/releases)\n[![License](https://img.shields.io/github/license/ramiawar/pydastic)](https://github.com/ramiawar/pydastic/blob/master/LICENSE)\n![Coverage Report](https://github.com/RamiAwar/pydastic/raw/main/assets/images/coverage.svg)\n\nPydastic is an elasticsearch python ORM based on Pydantic.\n\n</div>\n\n## 💾 Installation\n\nPip:\n```bash\npip install pydastic\n```\n\nPoetry:\n```bash\npoetry add pydastic\n```\n\n\n## 🚀 Features\n- Simple CRUD operations supported\n\n\n## 📋 Usage\n\n### Defining Models\n```python\nclass User(ESModel):\n    name: str\n    phone: Optional[str]\n    last_login: datetime = Field(default_factory=datetime.now)\n\n    class Meta:\n        index = "user"\n```\n\n### CRUD: Create, Update\n```python\nes = Elasticsearch(hosts="localhost:9200")\n\n# Create and save doc\nuser = User(name="John", age=20)\nuser.save(es, wait_for=True)\nassert user.id != None\n\n# Update doc\nuser.name = "Sam"\nuser.save(es, wait_for=True)\n```\n\n### Get Document\n```python\ngot = User.get(es, id=user.id)\nassert got == user\n```\n\n### CRUD: Delete\n```Not yet implemented.```\n\n\n## 📈 Releases\n\nNone yet.\n\nYou can see the list of available releases on the [GitHub Releases](https://github.com/ramiawar/pydastic/releases) page.\n\nWe follow [Semantic Versions](https://semver.org/) specification.\n\nWe use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.\n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/ramiawar/pydastic)](https://github.com/ramiawar/pydastic/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/ramiawar/pydastic/blob/master/LICENSE) for more details.\n\n## 📃 Citation\n\n```bibtex\n@misc{pydastic,\n  author = {Rami Awar},\n  title = {Pydastic is an elasticsearch python ORM based on Pydantic.},\n  year = {2022},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/ramiawar/pydastic}}\n}\n```\n',
    'author': 'pydastic',
    'author_email': 'rami.awar.ra@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ramiawar/pydastic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
