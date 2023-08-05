# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ballchaser']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=1.11.1,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'ballchaser',
    'version': '0.8.0',
    'description': 'Unofficial Python API client for the ballchasing.com API.',
    'long_description': '# ballchaser ⚽️🚗\n\n![PyPI](https://img.shields.io/pypi/v/ballchaser)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat)](https://pycqa.github.io/isort/)\n\nUnofficial Python API client for the ballchasing.com API.\n\n# Usage\n```commandline\npip install ballchaser\n```\n\nAll API requests are exposed via the `BallChaser` class which is initialised with a [ballchasing.com API token](https://ballchasing.com/doc/api#header-authentication).\n\n```python\nimport os\n\nfrom ballchaser.client import BallChaser\n\nball_chaser = BallChaser(os.getenv("BALLCHASING_API_TOKEN"))\n\n# search and retrieve replay metadata\nreplays = [\n    replay\n    for replay in ball_chaser.list_replays(player_name="GarrettG", replay_count=10)\n]\n\n# retrieve replay statistics\nreplay_stats = [\n    ball_chaser.get_replay(replay["id"])\n    for replay in replays\n]\n```\n\nAPI requests can automatically be retried if they return a rate limit response by specifying `backoff=True`. Requests\nwill be tried up to `max_tries` times with exponential backoff between subsequent retries, e.g.\n\n```python\nimport os\n\nfrom ballchaser.client import BallChaser\n\nball_chaser = BallChaser(os.getenv("BALLCHASING_API_TOKEN"), backoff=True, max_tries=5)\n```\n\n# Contributing & Feedback\n\nIf there are any new features you\'d like, or you encounter a bug, you can contribute by opening an issue or submitting a pull request.\n',
    'author': 'Tom Boyes-Park',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tom-boyes-park/ballchaser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
