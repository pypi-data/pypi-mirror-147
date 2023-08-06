# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4.0,<0.5.0', 'inquirer>=2.9.1,<3.0.0']

extras_require = \
{':python_version >= "3.8" and python_version < "4.0"': ['rich>=11.2.0,<12.0.0']}

entry_points = \
{'console_scripts': ['uhabits_converter = src.cli:main']}

setup_kwargs = {
    'name': 'uhabits-converter',
    'version': '0.2.2',
    'description': 'convert types of habit from uhabits',
    'long_description': '# uhabits_converter\n[![Build Status](https://github.com/ConorSheehan1/uhabits_converter/workflows/ci/badge.svg)](https://github.com/ConorSheehan1/uhabits_converter/actions/)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Tested Operating Systems](https://img.shields.io/badge/dynamic/yaml?url=https://raw.githubusercontent.com/ConorSheehan1/uhabits_converter/main/.github/workflows/ci.yml&label=os&query=$.jobs.build.strategy.matrix.os)](https://github.com/ConorSheehan1/uhabits_converter/blob/main/.github/workflows/ci.yml#L25)\n[![Tested python versions](https://img.shields.io/badge/dynamic/yaml?url=https://raw.githubusercontent.com/ConorSheehan1/uhabits_converter/main/.github/workflows/ci.yml&label=Tested%20python%20versions&query=$.jobs.build.strategy.matrix.python)](https://github.com/ConorSheehan1/uhabits_converter/blob/main/.github/workflows/ci.yml#L26)\n\n[Loop Habit / uhabits](https://github.com/iSoron/uhabits) converter.\n\n## Warnings\nPlease back up your data! By default this project does copy your data to a new db before editing it, but I make no promises it won\'t break on write or import.\n\nThis project is developed in my spare time, so it could be out of sync with [Loop Habit / uHabits](https://github.com/iSoron/uhabits).\nIt has been tested with version [2.0.3](https://github.com/iSoron/uhabits/releases/tag/v2.0.3).\n\n\n## Features\n1. Convert boolean habits to the new numeric habit type.\n    **Example output**\n    | Before                                          | After                                         |\n    | ----------------------------------------------- | --------------------------------------------- |\n    | ![coffee_bool](.github/images/coffee_bool.jpg)  | ![coffee_num](.github/images/coffee_num.jpg)  |\n\n\n## Installation\n```bash\n# option 1 github release\npip install https://github.com/ConorSheehan1/uhabits_converter/releases/latest/download/uhabits_converter.tar.gz\n\n# option 2 from source\n# install python (>=3.8 check pyproject.toml)\n# https://github.com/ConorSheehan1/uhabits_converter/blob/main/pyproject.toml#L9\ngit clone git@github.com:ConorSheehan1/uhabits_converter.git\ncd uhabits_converter\npoetry install\n# if you want the uhabits_converter command available run the lines below.\n# otherwise you can use: PYTHONPATH=$(pwd) poetry run task dev\npoetry build\npip install .\n```\n\n### Steps to convert habits\n1. Follow the instructions for **How can I export a full backup of my data?**\n    1. https://github.com/iSoron/uhabits/discussions/689 \n    > Select the option "Export full backup" on the settings screen.\n2. Copy the `.db` file to your computer\n3. Run `uhabits_converter` from a terminal\n    1. You can specify arguments up front or interactively. e.g.\n    `uhabits_converter --db=Loop_Habits_Backup_2022-02-28_220305.db --habits=Gym,Coffee`\n    this will convert the habits Gym and Coffee from boolean to numeric habits.\n    now you can track hours in the gym and cups of coffee, rather than just the days you went to the Gym or drank coffee.\n4. copy the `output.db` file back to your android device.\n5. follow the instructions for **How can I restore a full backup?**\n    > First, go to the settings screen and tap "Import data". A file browser should appear. Tap the menu icon (the one with three vertical lines) and select the app where your backup is stored, such as Google Drive.\n\n    > If your backup file is located in your SD card, after tapping "Import data", tap the icon with three dots on the top right corner of the screen and select "Show internal storage". Then, tap the menu icon (the one with three vertical lines) and select your SD card.\n\n\n### Development\nSee [DEV.md](./DEV.md)\n',
    'author': 'Conor Sheehan',
    'author_email': 'conor.sheehan.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ConorSheehan1/uhabits_converter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
