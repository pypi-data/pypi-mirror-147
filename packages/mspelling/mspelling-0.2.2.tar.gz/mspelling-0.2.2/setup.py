# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mspelling', 'mspelling.ui']

package_data = \
{'': ['*'], 'mspelling': ['stimuli/audio/*', 'stimuli/words/*']}

install_requires = \
['Kivy>=2.0.0,<3.0.0',
 'click>=8.0.3,<9.0.0',
 'kivymd>=0.104.2,<0.105.0',
 'numpy>=1.21.5,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'xlrd>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['mspelling = mspelling.main:main']}

setup_kwargs = {
    'name': 'mspelling',
    'version': '0.2.2',
    'description': 'Measure of Spanish spelling skills',
    'long_description': "# mSpelling\n\n[![PyPI - Version](https://img.shields.io/pypi/v/mspelling.svg)](https://pypi.python.org/pypi/mspelling)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mspelling.svg)](https://pypi.python.org/pypi/mspelling)\n![GitHub](https://img.shields.io/github/license/mario-bermonti/mspelling)\n[![Tests](https://github.com/mario-bermonti/mspelling/workflows/tests/badge.svg)](https://github.com/mario-bermonti/mspelling/actions?workflow=tests)\n[![Codecov](https://codecov.io/gh/mario-bermonti/mspelling/branch/master/graph/badge.svg?token=YOURTOKEN)](https://codecov.io/gh/mario-bermonti/mspelling)\n[![Read the Docs](https://readthedocs.org/projects/mspelling/badge/)](https://mspelling.readthedocs.io/)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\nMeasure of Spanish spelling skills\n\n* GitHub repo: <https://github.com/mario-bermonti/mspelling.git>\n* Documentation: <https://mspelling.readthedocs.io/>\n* Free software: GNU General Public License v3\n\n## Features\n- Developed specifically for research on spelling skills\n- Easy to administer\n- Flexible and easy to extend\n- Supports multiple platforms: MacOS, Windows, Linux\n- Results are saved to a CSV file\n\n## Description\n\n![demo](./mspelling_gif.gif)\n\nWords are presented by the computer one at a time and the participant types the word\nusing the keyboard. Participants have a rest period after every 5 trials.\n\nAt the end of the session, mspelling saves the results to a CSV file, which is supported\nby most popular spreadsheet software these days (e.g., Excel).\n\nmSpelling is developed using the Python programming language v3.\n\n## Getting Started\nPlease see [mSpelling documentation][project_docs] for details about how to install and use mSpelling.\n\n## Contributing to this project\n  All contributions are welcome!\n\n  Will find a detailed description of all the ways you can contribute to mspelling in\n  [the contributing guide][contributing_guide].\n\n  This is a beginner-friendly project so don't hesitate to ask any questions or get in touch\n  with the project's maintainers.\n\n  Please review the [project's code of conduct][code_conduct] before making\n  any contributions.\n\n## Author\nThis project was developed by Mario E. Bermonti-Pérez as part of\nhis academic research. Feel free to contact me at [mbermonti@psm.edu](mailto:mbermonti@psm.edu) or\n[mbermonti1132@gmail.com](mailto:mbermonti1132@gmail.com)\n\n## Credits\n\nThis package was created with [Cookiecutter][cookiecutter] and the [mario-bermonti/cookiecutter-modern-pypackage][cookiecutter-modern-pypackage] project template.\n\n[cookiecutter]: https://github.com/cookiecutter/cookiecutter\n[cookiecutter-modern-pypackage]: https://github.com/mario-bermonti/cookiecutter-modern-pypackage\n[project_docs]: https://mspelling.readthedocs.io/\n[code_conduct]: ./CODE_OF_CONDUCT.md\n[contributing_guide]: ./contributing.md\n",
    'author': 'Mario E. Bermonti Pérez',
    'author_email': 'mbermonti1132@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mario-bermonti/mspelling',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
