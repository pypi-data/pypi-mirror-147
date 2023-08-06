# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nbr', 'nbr.schemas', 'nbr.utils']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0',
 'nbformat>=5.3.0,<6.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'websockets>=10.2,<11.0']

setup_kwargs = {
    'name': 'nbr',
    'version': '0.0.1b0',
    'description': 'Jupyter notebooks runner',
    'long_description': '[![CI](https://github.com/zhivykh/nbr/workflows/CI/badge.svg)](https://github.com/zhivykh/nbr/actions/workflows/main.yml)\n[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\n# nbr\nNBR lets you **run** local and remote jupyter-notebooks.\n\n## Installation\nIn a terminal, run:\n```\npython3 -m pip install nbr\n```\n\n## Usage\n\nLaunch a Jupyter server:\n```\njupyter server --ServerApp.token=\'\' --ServerApp.password=\'\' --ServerApp.disable_check_xsrf=True\n```\n\nExecution a local notebook, using a remote server:\n\n\n```python\nimport nbr\nimport nbformat\nimport asyncio\n\nasync def main() -> None:\n    nb_file = nbformat.read("Untitled.ipynb", as_version=4)\n    \n    async with nbr.NotebookRunner(host="127.0.0.1", port=8888) as runner:\n        result = await runner.execute(cells=nb_file.cells)\n        \n        nb_file.cells = result.executed_cells\n        nbformat.write(nb_file, "executed_notebook.ipynb")\n    \nif __name__ == "__main__":\n    asyncio.run(main())\n```',
    'author': 'zhivykh',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zhivykh/nbr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
