# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autowoe',
 'autowoe.lib',
 'autowoe.lib.cat_encoding',
 'autowoe.lib.optimizer',
 'autowoe.lib.pipelines',
 'autowoe.lib.report',
 'autowoe.lib.report.utilities_images',
 'autowoe.lib.selectors',
 'autowoe.lib.types_handler',
 'autowoe.lib.utilities',
 'autowoe.lib.woe']

package_data = \
{'': ['*']}

install_requires = \
['StrEnum>=0.4.7,<0.5.0',
 'jinja2',
 'joblib',
 'lightgbm',
 'matplotlib',
 'numpy',
 'pandas',
 'pytest',
 'pytz',
 'scikit-learn',
 'scipy',
 'seaborn',
 'sphinx',
 'sphinx-rtd-theme',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'autowoe',
    'version': '1.3.2',
    'description': 'Library for automatic interpretable model building (Whitebox AutoML)',
    'long_description': "## AutoWoE library\n\n![PyPI - Downloads](https://img.shields.io/pypi/dm/autowoe?color=green&label=PyPI%20downloads&logo=pypi&logoColor=orange&style=plastic)\n\n\nThis is the repository for **AutoWoE** library, developed by LightAutoML group. This library can be used for automatic creation of interpretable ML model based on feature binning, WoE features transformation, feature selection and Logistic Regression.\n\n**Authors:** Vakhrushev Anton, Grigorii Penkin, Alexander Kirilin\n\n**Library setup** can be done by one of three scenarios below:\n\n1. Installation from PyPI:\n```bash\npip install autowoe\n```\n2. Installation from source code\n\nFirst of all you need to install [git](https://git-scm.com/downloads) and [poetry](https://python-poetry.org/docs/#installation).\n\n```bash\n\n# Load LAMA source code\ngit clone https://github.com/AILab-MLTools/AutoMLWhitebox.git\n\ncd AutoMLWhiteBox/\n\n# !!!Choose only one item!!!\n\n# 1. Recommended: Create virtual environment inside your project directory\npoetry config virtualenvs.in-project true\n\n# 2. Global installation: Don't create virtual environment\npoetry config virtualenvs.create false --local\n\n# For more information read poetry docs\n\n# Install WhiteBox\npoetry install\n\n```\n\n\n**Usage tutorials** are in Jupyter notebooks in the repository root. For **parameters description** take a look at `parameters_info.md`.\n\n**Bugs / Questions / Suggestions:**:\n- Vakhrushev Anton (btbpanda@gmail.com)\n",
    'author': 'Vakhrushev Anton',
    'author_email': 'btbpanda@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AILab-MLTools/AutoMLWhitebox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
