# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mkdocs_matplotlib']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1',
 'mkdocs-material>=8.2.8',
 'mkdocs>=1.3.0',
 'seaborn>=0.11.2,<0.12.0']

entry_points = \
{'mkdocs.plugins': ['mkdocs_matplotlib = '
                    'mkdocs_matplotlib.plugin:RenderPlugin']}

setup_kwargs = {
    'name': 'mkdocs-matplotlib',
    'version': '0.3.0',
    'description': 'Live rendering of python code using matplotlib',
    'long_description': '# Mkdocs-Matplotlib\n\n**Mkdocs-Matplotlib** is a plugin for [mkdocs](https://www.mkdocs.org/) which allows you to automatically generate matplotlib figures and add them to your documentation.\nSimply write the code as markdown into your documention.\n\n![screenshot](docs/assets/screenshot.png)\n\n## Quick Start\n\nThis plugin can be installed with `pip`\n\n```shell\npip install mkdocs-matplotlib\n```\nTo enable this plugin for mkdocs you need to add the following lines to your `mkdocs.yml`.\n\n```yaml\nplugins:\n  - mkdocs_matplotlib\n```\n\nTo render a code cell using matplotlib you simply have to add the comment `# mkdocs: render` at the top of the cell.\n\n```python\n# mkdocs: render\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nxpoints = np.array([1, 8])\nypoints = np.array([3, 10])\n\nplt.plot(xpoints, ypoints)\n```\n',
    'author': 'An Hoang',
    'author_email': 'an.hoang@statworx.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.9,<3.9.0',
}


setup(**setup_kwargs)
