# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typepigeon']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil']

extras_require = \
{':python_version <= "3.7"': ['importlib_metadata'],
 'development': ['isort', 'oitnb'],
 'documentation': ['m2r2', 'sphinx', 'sphinx-rtd-theme'],
 'spatial': ['pyproj', 'shapely'],
 'testing': ['pytest', 'pytest-cov', 'pytest-xdist']}

setup_kwargs = {
    'name': 'typepigeon',
    'version': '0.0.0',
    'description': 'Python type converter',
    'long_description': '# TypePigeon\n\n[![tests](https://github.com/zacharyburnett/TypePigeon/workflows/tests/badge.svg)](https://github.com/zacharyburnett/TypePigeon/actions?query=workflow%3Atests)\n[![codecov](https://codecov.io/gh/zacharyburnett/TypePigeon/branch/main/graph/badge.svg?token=4DwZePHp18)](https://codecov.io/gh/zacharyburnett/TypePigeon)\n[![build](https://github.com/zacharyburnett/TypePigeon/workflows/build/badge.svg)](https://github.com/zacharyburnett/TypePigeon/actions?query=workflow%3Abuild)\n[![version](https://img.shields.io/pypi/v/TypePigeon)](https://pypi.org/project/TypePigeon)\n[![Anaconda-Server Badge](https://anaconda.org/conda-forge/typepigeon/badges/version.svg)](https://anaconda.org/conda-forge/typepigeon)\n[![license](https://img.shields.io/github/license/zacharyburnett/TypePigeon)](https://creativecommons.org/share-your-work/public-domain/cc0)\n[![style](https://sourceforge.net/p/oitnb/code/ci/default/tree/_doc/_static/oitnb.svg?format=raw)](https://sourceforge.net/p/oitnb/code)\n\nTypePigeon is a Python type converter focused on converting values between\nvarious Python data types.\n\n```shell\npip install typepigeon\n```\n\n## Features\n\n- convert values directly from one Python type to another with `convert_value()`\n- convert values to JSON format with `convert_to_json()`\n- convert generic aliases (`List[str]`) to simple collection types (`[str]`)\n  with `guard_generic_alias()`\n\n## Usage\n\nWith TypePigeon, you can convert simple values from one type to another:\n\n### `convert_value()`\n\n```python\nimport typepigeon\n\ntypepigeon.convert_value(0.55, str)\n\'0.55\'\n\ntypepigeon.convert_value(1, float)\n1.0\n\ntypepigeon.convert_value([1], str)\n\'[1]\'\n```\n\nAdditionally, you can also cast values into a collection:\n\n```python\nimport typepigeon\n\ntypepigeon.convert_value([1, 2.0, \'3\'], [int])\n[1, 2, 3]\n\ntypepigeon.convert_value(\'[1, 2, 3]\', (int, str, float))\n[1, \'2\', 3.0]\n\ntypepigeon.convert_value({\'a\': 2.5, \'b\': 4, 3: \'18\'}, {str: float})\n{\'a\': 2.5, \'b\': 4.0, \'3\': 18.0}\n```\n\nSome commonly-used classes such as `datetime` and `CRS` are also supported:\n\n```python\nfrom datetime import datetime, timedelta\n\nfrom pyproj import CRS\nimport typepigeon\n\ntypepigeon.convert_value(datetime(2021, 3, 26), str)\n\'2021-03-26 00:00:00\'\n\ntypepigeon.convert_value(\'20210326\', datetime)\ndatetime(2021, 3, 26)\n\ntypepigeon.convert_value(\'01:13:20:00\', timedelta)\ntimedelta(days=1, hours=13, minutes=20, seconds=0)\n\ntypepigeon.convert_value(timedelta(hours=1), str)\n\'01:00:00.0\'\n\ntypepigeon.convert_value(timedelta(hours=1), int)\n3600\n\ntypepigeon.convert_value(CRS.from_epsg(4326), int)\n4326\n\ntypepigeon.convert_value(CRS.from_epsg(4326), str)\n\'GEOGCRS["WGS 84",ENSEMBLE["World Geodetic System 1984 ensemble",MEMBER["World Geodetic System 1984 (Transit)"],MEMBER["World Geodetic System 1984 (G730)"],MEMBER["World Geodetic System 1984 (G873)"],MEMBER["World Geodetic System 1984 (G1150)"],MEMBER["World Geodetic System 1984 (G1674)"],MEMBER["World Geodetic System 1984 (G1762)"],ELLIPSOID["WGS 84",6378137,298.257223563,LENGTHUNIT["metre",1]],ENSEMBLEACCURACY[2.0]],PRIMEM["Greenwich",0,ANGLEUNIT["degree",0.0174532925199433]],CS[ellipsoidal,2],AXIS["geodetic latitude (Lat)",north,ORDER[1],ANGLEUNIT["degree",0.0174532925199433]],AXIS["geodetic longitude (Lon)",east,ORDER[2],ANGLEUNIT["degree",0.0174532925199433]],USAGE[SCOPE["Horizontal component of 3D system."],AREA["World."],BBOX[-90,-180,90,180]],ID["EPSG",4326]]\'\n\ntypepigeon.convert_value(4326, CRS)\nCRS.from_epsg(4326)\n```\n\n### `convert_to_json()`\n\n```python\nfrom datetime import datetime\n\nimport typepigeon\n\ntypepigeon.convert_to_json(5)\n5\n\ntypepigeon.convert_to_json(\'5\')\n\'5\'\n\ntypepigeon.convert_to_json(datetime(2021, 3, 26))\n\'2021-03-26 00:00:00\'\n\ntypepigeon.convert_to_json([5, \'6\', {3: datetime(2021, 3, 27)}])\n[5, \'6\', {3: \'2021-03-27 00:00:00\'}]\n\ntypepigeon.convert_to_json({\'test\': [5, \'6\', {3: datetime(2021, 3, 27)}]})\n{\'test\': [5, \'6\', {3: \'2021-03-27 00:00:00\'}]}\n```\n\n### `guard_generic_alias()`\n\n```python\nfrom typing import Dict, List, Tuple\n\nimport typepigeon\n\ntypepigeon.guard_generic_alias(List[str])\n[str]\n\ntypepigeon.guard_generic_alias(Dict[str, float])\n{str: float}\n\ntypepigeon.guard_generic_alias({str: (Dict[int, str], str)})\n{str: ({int: str}, str)}\n```',
    'author': 'Zach Burnett',
    'author_email': 'zachary.r.burnett@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zacharyburnett/TypePigeon.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
