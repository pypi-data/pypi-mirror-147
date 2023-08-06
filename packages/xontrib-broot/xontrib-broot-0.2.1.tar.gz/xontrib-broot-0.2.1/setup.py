# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xontrib']

package_data = \
{'': ['*']}

install_requires = \
['xonsh>=0.12']

setup_kwargs = {
    'name': 'xontrib-broot',
    'version': '0.2.1',
    'description': 'broot support function for xonsh shell',
    'long_description': '# Overview\n[broot](https://github.com/Canop/broot) support function for xonsh shell\n\n\n## Installation\n\nTo install use pip:\n\n``` bash\nxpip install xontrib-broot\n# or: xpip install -U git+https://github.com/jnoortheen/xontrib-broot\n```\n\n## Usage\nIt adds `br` alias function. So commands like `cd` will work from broot.\n``` bash\n$ xontrib load broot\n$ br \n```\n\n`broot` can also be launched with shortcut `Ctrl+N`. \nThis can be changed by `$XONSH_BROOT_KEY="c-n"` or disabled with `$XONSH_BROOT_KEY=""`. \n(PS [PTK\'s keybinding guide](https://python-prompt-toolkit.readthedocs.io/en/master/pages/advanced_topics/key_bindings.html#list-of-special-keys) \nfor full list of key names.)\n\n## Credits\n\nThis package was created with [xontrib cookiecutter template](https://github.com/jnoortheen/xontrib-cookiecutter).\n',
    'author': 'Noortheen Raja NJ',
    'author_email': 'jnoortheen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jnoortheen/xontrib-broot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
