# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nbr', 'nbr.schemas', 'nbr.utils']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0', 'pydantic>=1.9.0,<2.0.0', 'websockets>=10.2,<11.0']

extras_require = \
{'nbformat': ['nbformat>=5.3.0,<6.0.0']}

setup_kwargs = {
    'name': 'nbr',
    'version': '0.0.2b0',
    'description': 'Jupyter notebooks runner',
    'long_description': '[![CI](https://github.com/zhivykh/nbr/workflows/CI/badge.svg)](https://github.com/zhivykh/nbr/actions/workflows/main.yml)\n[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)\n[![Stable Version](https://img.shields.io/pypi/v/nbr?color=blue)](https://pypi.org/project/nbr/)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\n# nbr\nNBR lets you **run** local and remote jupyter-notebooks.\n\n## Installation\nIn a terminal, run:\n```\npip install nbr\n```\n\n## Usage\n\nLaunch a Jupyter server:\n```\njupyter server\n```\n\nExecution a local notebook, using a remote server:\n\n\n```python\nimport asyncio\nfrom nbr import NotebookRunner, Notebook\n\n\nasync def main() -> None:\n    notebook = Notebook.read_file(name="Untitled.ipynb")\n\n    async with NotebookRunner(\n        notebook=notebook,\n        host="127.0.0.1",\n        port=8888,\n        token="481145d4be3c79620c23e2bb4e5b818a3669c4e88ea75c35",\n    ) as runner:\n        result = await runner.execute_all_cells()\n        print(result.status)\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```',
    'author': 'Nick Zhivykh',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zhivykh/nbr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
