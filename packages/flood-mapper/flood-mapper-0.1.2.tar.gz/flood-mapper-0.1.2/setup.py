# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flood_mapper']

package_data = \
{'': ['*']}

install_requires = \
['earthengine-api>=0.1.288,<0.2.0']

setup_kwargs = {
    'name': 'flood-mapper',
    'version': '0.1.2',
    'description': '',
    'long_description': "# flood-mapper\n\nDetect flood extents on Sentinel-1 satellite imagery using the [recommended method from United Nations UN-SPIDER Knowledge Portal](https://un-spider.org/advisory-support/recommended-practices/recommended-practice-google-earth-engine-flood-mapping/step-by-step#Step%202:%20Time%20frame%20and%20sensor%20parameters%20selection\n).\n\n## Installation\n\n`pip install flood-mapper`\n\n\n## Usage\n\n```python\nimport ee\nfrom flood_mapper import derive_flood_extents\n\nee.Initialize()\nee.Authenticate()\n\n# Define a start and end date between to select imagery before the flooding event\nbefore_start = '2020-10-01'\nbefore_end = '2020-10-15'\n\n# Define a start and end date between to select imagery after the flooding event\nafter_start = '2020-11-04'\nafter_end = '2020-11-15'\n\n# Define a geographic region where the flooding occurred.\nregion = ee.Geometry.Polygon([[[-85.93, 16.08],\n                               [-85.93, 15.69],\n                               [-85.40, 15.69],\n                               [-85.40, 16.08]]])\n\n# Change the export flag to 'False' if you do not wish to export the results to Google Drive\ndetected_flood_vector, detected_flood_raster, before_imagery, after_imagery = derive_flood_extents(region,\n                                                                                                   before_start,\n                                                                                                   before_end,\n                                                                                                   after_start,\n                                                                                                   after_end,\n                                                                                                   export=True,\n                                                                                                   export_filename='my_filename')\n\n```",
    'author': 'cate',
    'author_email': 'catherineseale@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cateseale/flood-mapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
