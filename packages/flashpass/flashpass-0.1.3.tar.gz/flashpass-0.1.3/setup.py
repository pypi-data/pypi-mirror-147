# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flashpass']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=36.0.2,<37.0.0', 'pyperclip>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['flashpass = flashpass.cli:main']}

setup_kwargs = {
    'name': 'flashpass',
    'version': '0.1.3',
    'description': 'Encrypt & Decrypt FlashPass .fp files',
    'long_description': '=========\nFlashPass\n=========\n\nFlashPass is a simple cross-platform password manager written in Python.\n\nDecrypted passwords are copied to your clipboard.\n\n************\nInstallation\n************\n\nInstall from PyPi:\n\n.. code-block:: console\n\n  pip install flashpass\n\nOr, from the release tarball/wheel:\n\n* Download the `latest release <https://github.com/Septem151/flashpass/releases/latest>`_\n* Navigate to the directory where you saved the release\n* ``pip install --upgrade [release file]``\n\n*****\nUsage\n*****\n\nInteractive mode\n================\n\n* ``flashpass``\n\nStandard mode of FlashPass, guided prompts for password encryption/decryption.\n\nEncrypt a new password\n======================\n\n* ``flashpass -e [name]`` or ``flashpass --encrypt [name]``\n\nEncrypts a new password with the given name.\n\nDecrypt an existing password\n============================\n\n* ``flashpass -d [name]`` or ``flashpass --decrypt [name]``\n\nDecrypts an existing password with the given name and copies the password to your clipboard.\n\nList all stored passwords\n=========================\n\n* ``flashpass -l`` or ``flashpass --list``\n\nList the names of all stored passwords.\n\nPrint help\n==========\n\n* ``flashpass -h`` or ``flashpass --help``\n\nPrint all available commands and their descriptions.\n',
    'author': 'Carson Mullins',
    'author_email': 'carsonmullins@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Septem151/flashpass',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
