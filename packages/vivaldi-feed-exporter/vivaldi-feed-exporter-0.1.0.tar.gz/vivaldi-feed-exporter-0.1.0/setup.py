# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vivaldi_feed_exporter']

package_data = \
{'': ['*']}

install_requires = \
['opyml>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['vivaldi-feed-exporter = vivaldi_feed_exporter.main:run']}

setup_kwargs = {
    'name': 'vivaldi-feed-exporter',
    'version': '0.1.0',
    'description': 'A command line tool to export feeds from Vivaldi as OPML',
    'long_description': "# vivaldi-feed-exporter\n\nSince [Vivaldi](https://vivaldi.com) does not currently have the ability to export feeds,\nI created a command line tool to generate [OPML](http://opml.org) based on a profile.\n\n*Disclaimer : It depends on Vivaldi's implementation, so it may stop working at any time*\n\n## Usage\n\n- Follow [this page](https://help.vivaldi.com/desktop/tools/import-and-export-browser-data/#Transfer_the_full_Vivaldi_browser_profile) \n  to identify your Vivaldi profile folder\n- Install `vivaldi-feed-exporter` via `pipx install vivaldi-feed-exporter`\n- Running `vivaldi-feed-exporter <profile folder path>` will output OPML to standard output\n\n## Mapping of Vivaldi feed properties to OPML `outline` element attributes\n\nVivaldi feed property |`outline` attribute\n-|-\ntitle|`text`, `title`\naddress|`xmlUrl`\n",
    'author': 'Akira Takahashi',
    'author_email': 'pretty.audience.64b9de@gizmotik.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/a-takahashi223/vivaldi-feed-exporter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
