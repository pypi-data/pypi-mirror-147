# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['keyring_subprocess',
 'keyring_subprocess._internal',
 'keyring_subprocess._vendor',
 'keyring_subprocess._vendor.importlib_metadata',
 'keyring_subprocess._vendor.keyring',
 'keyring_subprocess._vendor.keyring.backends',
 'keyring_subprocess._vendor.keyring.backends.macOS',
 'keyring_subprocess._vendor.keyring.testing',
 'keyring_subprocess._vendor.keyring.util',
 'keyring_subprocess.backend']

package_data = \
{'': ['*']}

entry_points = \
{'keyring.backends': ['keyring-subprocess = '
                      'keyring_subprocess.backend:SubprocessBackend'],
 'sitecustomize': ['keyring-subprocess = '
                   'keyring_subprocess._internal:sitecustomize'],
 'virtualenv.seed': ['keyring-subprocess = '
                     'keyring_subprocess._internal:KeyringSubprocessFromAppData']}

setup_kwargs = {
    'name': 'keyring-subprocess',
    'version': '0.2.0',
    'description': '',
    'long_description': "# keyring-subprocess\nA dependency keyring backend that queries an executable `keyring` which can be\nfound on PATH.\n\n## Pros\n- Zero dependencies for a clean `pip list` command and should always be\n  compatible with the rest of your dependencies. Which makes it more\n  suitable to be added to `PYTHONPATH` after installing with Pip's\n  `--target` flag.\n- Has [keyring](https://pypi.org/project/keyring) and the minimal required\n  dependencies vendored to make the `chainer` and `null` backends work.\n  - It uses the ModuleSpec apis provided by [PEP451](https://peps.python.org/pep-0451/)\n    to make the vendored `keyring` importable.\n- Provides a `virtualenv` [Seeder](https://virtualenv.pypa.io/en/latest/user_guide.html#seeders)\n  named `keyring-subprocess`.\n\n## Cons\n- It does require `keyring-subprocess` to be installed in the virtual\n  environment associated with the `keyring` executable that is found.\n- Adds or replaces points of failures depending on how you look at it.\n- Being able to import `keyring`, `importlib_metadata` and `zipp` but\n  `pip list` not listing them might be confusing and not very helpful during\n  debugging.\n",
    'author': 'Dos Moonen',
    'author_email': 'darsstar@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://keyring-subprocess.darsstar.dev/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
