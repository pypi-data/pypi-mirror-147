# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airflint', 'airflint.rules']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0', 'refactor>=0.4.3,<0.5.0']

entry_points = \
{'console_scripts': ['airflint = airflint.__main__:main']}

setup_kwargs = {
    'name': 'airflint',
    'version': '0.1.2a0',
    'description': 'Enforce Best Practices for all your Airflow DAGs. ⭐',
    'long_description': '# airflint\n\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/feluelle/airflint/main.svg)](https://results.pre-commit.ci/latest/github/feluelle/airflint/main)\n![test workflow](https://github.com/feluelle/airflint/actions/workflows/test.yml/badge.svg)\n![codeql-analysis workflow](https://github.com/feluelle/airflint/actions/workflows/codeql-analysis.yml/badge.svg)\n[![codecov](https://codecov.io/gh/feluelle/airflint/branch/main/graph/badge.svg?token=J8UEP8IVY4)](https://codecov.io/gh/feluelle/airflint)\n[![PyPI version](https://img.shields.io/pypi/v/airflint)](https://pypi.org/project/airflint/)\n[![License](https://img.shields.io/pypi/l/airflint)](https://github.com/feluelle/airflint/blob/main/LICENSE)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/airflint)](https://pypi.org/project/airflint/)\n[![PyPI version](https://img.shields.io/pypi/dm/airflint)](https://pypi.org/project/airflint/)\n\n> Enforce Best Practices for all your Airflow DAGs. ⭐\n\n## 🧑\u200d🏫 Rules\n\n- [x] use datetime instead of days_ago in DAG start_date\n- [x] task decorator instead of PythonOperator and PythonVenvOperator\n- [x] dag decorator instead of DAG\n- [x] jinja string instead of Variable.get\n\n> ⚠️ airflint does not remove imports. For removing unused imports please use [autoflake](https://github.com/PyCQA/autoflake) additionally.\n\nPlease check the [known issues](KNOWN_ISSUES.md) first, in case you find any bugs. If you cannot find them there, please open an Issue.\n\n## 💡 Future Ideas\n\n- fix Official Airflow `DeprecationWarning`s\n\n## 🚀 Get started\n\nTo install it from [PyPI](https://pypi.org/) run:\n\n```console\npip install airflint\n```\n\nThen just call it like this:\n\n![usage](assets/images/usage.png)\n\n### pre-commit\n\nAlternatively you can add the following repo to your `pre-commit-config.yaml`:\n\n```yaml\n  - repo: https://github.com/feluelle/airflint\n    rev: v0.1.1-alpha\n    hooks:\n      - id: airflint\n        args: ["-a"]  # Use -a for replacing inplace\n```\n',
    'author': 'Felix Uellendall',
    'author_email': 'feluelle@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
