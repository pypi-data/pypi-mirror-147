# SMAT-CLI
> Provides command line tools for getting data from the Social Media Analysis Toolkit ([SMAT](https://www.smat-app.com))
> as well as a library for interacting with SMAT from your own code.

[![Python Versions][python-image]](https://)
[![Latest Release][latest-release-image]](https://pypi.org/project/smat-cli/)
[![Pipeline Status][pipeline-status-image]](https://gitlab.com/dhosterman/smat-cli)

The [Social Media Analysis Toolkit](https://www.smat-app.com) is a resource that allows activists, journalists, 
researchers, and other social good organizations to collect information about hate, mis/disinformation, and extremism
from a variety of online platforms. The folks at SMAT are providing an amazing service and deserve your support! Go to
their [Open Collective](https://opencollective.com/smat) page to support them if you're able.

SMAT-CLI is a tool that makes getting that information from the API easy, either from your terminal or as part of your
own application.

## Installation

**OS X & Linux:**

```sh
pip install smat-cli
```

Though, I recommend using [Pipx](https://github.com/pypa/pipx) to install it as a a system tool.

```sh
pipx install smat-cli
```

**Windows:**

Coming soon!

## Usage Examples

Let's say you want to collect 1000 posts from Telegram posted between Jan 6 to March 1, 2021. You can do that with the 
`content` command like this.

```sh
smat content -s telegram -l 1000 --since 2021-01-06 --until 2021-03-01 trump
```

If you want some aggregated data, you can use the `timeseries` command to fetch a count of posts mentioning Trump from 
Jan 6 to March 1, 2021 and aggregate those into daily buckets, you can use the following.

```sh
smat timeseries -s telegram -i day --since 2021-01-06 --until 2021-03-01 trump
```

You can also aggregate by any arbitrary key present in the data for the site. To get an idea of which keys are available,
you can examine the results of a `content` command. Once you know the key you want to aggregate on, you can use `activity`
to, for example, count the number of posts containing the term Trump in each Telegram channel from Jan 6 to March 1, 2022.

```sh
smat activity -s telegram -a channelusername --since 2021-01-06 --until 2021-03-01 trump
```

All above commands print output line-by-line to stdout in JSON, so you can pipe the results to a file in the normal way.

```sh

smat content -s telegram -l 1000 --since 2021-01-06 --until 2021-03-01 trump >> data.ndjson
```

You can also specify different formats for the output. For example, if you'd like the results in JSON instead of 
JSONlines, you can pass `--format json`. This is currently the only way to format changepoint data when using 
`timeseries`.

```sh
smat --format json content -s telegram -l 1000 --since 2021-01-06 --until 2021-03-01 trump > data.json
```

In addition, this package can be used in another application by importing `Smat` from `smat_cli` and using it to query
the API from inside your program.

```python
from smat_cli import Smat
api = Smat()
data = api.content(term="trump", site="telegram", ...)
for d in data:
    print(d["message"])
```


## Development Setup

This project uses [Poetry](https://python-poetry.org/) and the code is formatted with [Black](https://github.com/psf/black).

Tests can be run via [Tox](https://tox.wiki/en/latest/), which will run the tests in Python verions: 3.7, 3.8, 3.9, 3.10.
For this to work properly, all of these Python versions must be installed. A Dockerfile has been included in the `test_runner`
directory if necessary.

```sh
poetry install
tox
```

## Release History

* 0.1.0
  * Initial release
* 0.1.1
  * Updates to package info and README
* 0.1.2
  * Updates to package info and README
  * Add formatters and JsonFormatter

## Me

Daniel Hosterman – [@dhosterman](https://twitter.com/dhosterman) – daniel@danielhosterman.com

Distributed under the [Unlicense](http://unlicense.org) license. See ``LICENSE`` for more information.

[https://gitlab.com/dhosterman](https://gitlab.com/dhosterman/)

## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Format your code with [Black](https://github.com/psf/black)
4. Ensure there are tests for your changes and that they pass
5. Commit your changes (`git commit -am 'Add some fooBar'`)
6. Push to the branch (`git push origin feature/fooBar`)
7. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[python-image]: https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-informational
[latest-release-image]: https://img.shields.io/badge/latest%20release-0.1.2-informational
[pipeline-status-image]: https://gitlab.com/dhosterman/smat-cli/badges/main/pipeline.svg
