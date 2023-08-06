# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smat_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<9.0.0', 'requests>=2.27.1,<3.0.0', 'urllib3>=1.26.9,<2.0.0']

entry_points = \
{'console_scripts': ['smat = smat_cli.cli:main']}

setup_kwargs = {
    'name': 'smat-cli',
    'version': '0.1.2',
    'description': 'A command line tool and library to get data from the Social Media Analysis Toolkit (SMAT).',
    'long_description': '# SMAT-CLI\n> Provides command line tools for getting data from the Social Media Analysis Toolkit ([SMAT](https://www.smat-app.com))\n> as well as a library for interacting with SMAT from your own code.\n\n[![Python Versions][python-image]](https://)\n[![Latest Release][latest-release-image]](https://pypi.org/project/smat-cli/)\n[![Pipeline Status][pipeline-status-image]](https://gitlab.com/dhosterman/smat-cli)\n\nThe [Social Media Analysis Toolkit](https://www.smat-app.com) is a resource that allows activists, journalists, \nresearchers, and other social good organizations to collect information about hate, mis/disinformation, and extremism\nfrom a variety of online platforms. The folks at SMAT are providing an amazing service and deserve your support! Go to\ntheir [Open Collective](https://opencollective.com/smat) page to support them if you\'re able.\n\nSMAT-CLI is a tool that makes getting that information from the API easy, either from your terminal or as part of your\nown application.\n\n## Installation\n\n**OS X & Linux:**\n\n```sh\npip install smat-cli\n```\n\nThough, I recommend using [Pipx](https://github.com/pypa/pipx) to install it as a a system tool.\n\n```sh\npipx install smat-cli\n```\n\n**Windows:**\n\nComing soon!\n\n## Usage Examples\n\nLet\'s say you want to collect 1000 posts from Telegram posted between Jan 6 to March 1, 2021. You can do that with the \n`content` command like this.\n\n```sh\nsmat content -s telegram -l 1000 --since 2021-01-06 --until 2021-03-01 trump\n```\n\nIf you want some aggregated data, you can use the `timeseries` command to fetch a count of posts mentioning Trump from \nJan 6 to March 1, 2021 and aggregate those into daily buckets, you can use the following.\n\n```sh\nsmat timeseries -s telegram -i day --since 2021-01-06 --until 2021-03-01 trump\n```\n\nYou can also aggregate by any arbitrary key present in the data for the site. To get an idea of which keys are available,\nyou can examine the results of a `content` command. Once you know the key you want to aggregate on, you can use `activity`\nto, for example, count the number of posts containing the term Trump in each Telegram channel from Jan 6 to March 1, 2022.\n\n```sh\nsmat activity -s telegram -a channelusername --since 2021-01-06 --until 2021-03-01 trump\n```\n\nAll above commands print output line-by-line to stdout in JSON, so you can pipe the results to a file in the normal way.\n\n```sh\n\nsmat content -s telegram -l 1000 --since 2021-01-06 --until 2021-03-01 trump >> data.ndjson\n```\n\nYou can also specify different formats for the output. For example, if you\'d like the results in JSON instead of \nJSONlines, you can pass `--format json`. This is currently the only way to format changepoint data when using \n`timeseries`.\n\n```sh\nsmat --format json content -s telegram -l 1000 --since 2021-01-06 --until 2021-03-01 trump > data.json\n```\n\nIn addition, this package can be used in another application by importing `Smat` from `smat_cli` and using it to query\nthe API from inside your program.\n\n```python\nfrom smat_cli import Smat\napi = Smat()\ndata = api.content(term="trump", site="telegram", ...)\nfor d in data:\n    print(d["message"])\n```\n\n\n## Development Setup\n\nThis project uses [Poetry](https://python-poetry.org/) and the code is formatted with [Black](https://github.com/psf/black).\n\nTests can be run via [Tox](https://tox.wiki/en/latest/), which will run the tests in Python verions: 3.7, 3.8, 3.9, 3.10.\nFor this to work properly, all of these Python versions must be installed. A Dockerfile has been included in the `test_runner`\ndirectory if necessary.\n\n```sh\npoetry install\ntox\n```\n\n## Release History\n\n* 0.1.0\n  * Initial release\n* 0.1.1\n  * Updates to package info and README\n* 0.1.2\n  * Updates to package info and README\n  * Add formatters and JsonFormatter\n\n## Me\n\nDaniel Hosterman – [@dhosterman](https://twitter.com/dhosterman) – daniel@danielhosterman.com\n\nDistributed under the [Unlicense](http://unlicense.org) license. See ``LICENSE`` for more information.\n\n[https://gitlab.com/dhosterman](https://gitlab.com/dhosterman/)\n\n## Contributing\n\n1. Fork it (<https://github.com/yourname/yourproject/fork>)\n2. Create your feature branch (`git checkout -b feature/fooBar`)\n3. Format your code with [Black](https://github.com/psf/black)\n4. Ensure there are tests for your changes and that they pass\n5. Commit your changes (`git commit -am \'Add some fooBar\'`)\n6. Push to the branch (`git push origin feature/fooBar`)\n7. Create a new Pull Request\n\n<!-- Markdown link & img dfn\'s -->\n[python-image]: https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-informational\n[latest-release-image]: https://img.shields.io/badge/latest%20release-0.1.2-informational\n[pipeline-status-image]: https://gitlab.com/dhosterman/smat-cli/badges/main/pipeline.svg\n',
    'author': 'dhosterman',
    'author_email': 'daniel@danielhosterman.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/dhosterman/smat-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
