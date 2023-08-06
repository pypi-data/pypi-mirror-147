"""
CLI for the SMAT API.
"""

import datetime

import click

from smat_cli import Smat, SmatError
from smat_cli.formatters import NdjsonFormatter, JsonFormatter


def until_default():
    return (datetime.date.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")


@click.group()
@click.option(
    "--format",
    "-f",
    default="ndjson",
    type=click.Choice(["ndjson", "json"]),
    help="Format to return data in.",
    show_default=True,
)
@click.pass_context
def main(ctx, format):
    """
    smat is a tool for querying the Social Media Analysis Toolkit (https://www.smat-app.com). It supports querying
    via the public API, which may be subject to rate limits, and responses may take substantial time if the server is
    busy. All commands can accept ElasticSearch query string syntax (see ElasticSearch documentation).

    \f
    This is the main Click group for the cli, accessible via the package's entrypoint "smat".
    """
    ctx.ensure_object(dict)
    formatters = {"ndjson": NdjsonFormatter, "json": JsonFormatter}
    ctx.obj["formatter"] = formatters[format]


@main.command()
@click.pass_context
@click.option(
    "--limit",
    "-l",
    default=10,
    type=int,
    help="Maximum number of results to return.",
    show_default=True,
)
@click.option(
    "--site",
    "-s",
    required=True,
    help="The site to get the content from.",
)
@click.option(
    "--since",
    default=until_default(),
    type=click.DateTime(),
    help="Earliest datetime of the content to return.",
    show_default=True,
)
@click.option(
    "--until",
    type=click.DateTime(),
    help="Latest datetime of the content to return.",
)
@click.argument("query", type=str)
def content(ctx, limit, site, since, until, query):
    """
    Get content matching a query from a site.

    \f
    A Click command for the main group that makes requests to the /content endpoint and outputs JSON results.
    """
    api = Smat()
    try:
        formatter = ctx.obj["formatter"](
            api.content(term=query, limit=limit, site=site, since=since, until=until)
        )
    except SmatError as e:
        click.echo("Error: " + str(e))

    for each in formatter.content():
        click.echo(each)


@main.command()
@click.pass_context
@click.option(
    "--site",
    "-s",
    required=True,
    help="The site to get the content from.",
)
@click.option(
    "--since",
    default=until_default(),
    type=click.DateTime(),
    help="Earliest datetime of the content to return.",
    show_default=True,
)
@click.option(
    "--until",
    type=click.DateTime(),
    help="Latest datetime of the content to return.",
)
@click.option(
    "--interval",
    "-i",
    type=str,
    help="Interval for the data being returned.",
)
@click.option(
    "--changepoint/--no-changepoint",
    type=bool,
    default=False,
    help="Include changepoint (only for json format).",
)
@click.argument("query", type=str)
def timeseries(ctx, query, interval, site, since, until, changepoint=False):
    """
    Get timeseries matching a query from a site.

    \f
    A Click command for the main group that makes requests to the /timeseries endpoint and outputs JSON results.
    """
    if not ctx.obj["formatter"] == JsonFormatter and changepoint:
        raise click.ClickException("`--changepoint` must be used with `--format json`")
    api = Smat()
    try:
        formatter = ctx.obj["formatter"](
            api.timeseries(
                term=query,
                since=since,
                until=until,
                interval=interval,
                site=site,
                changepoint=changepoint,
            )
        )
    except SmatError as e:
        click.echo("Error: " + str(e))

    for each in formatter.timeseries():
        click.echo(each)


@main.command()
@click.pass_context
@click.option(
    "--site",
    "-s",
    required=True,
    help="The site to get the content from.",
)
@click.option(
    "--since",
    default=until_default(),
    type=click.DateTime(),
    help="Earliest datetime of the content to return.",
    show_default=True,
)
@click.option(
    "--until",
    type=click.DateTime(),
    help="Latest datetime of the content to return.",
)
@click.option(
    "--agg-by",
    "-a",
    type=str,
    required=True,
    help="Response key to aggregate by.",
)
@click.argument("query", type=str)
def activity(ctx, query, site, since, until, agg_by):
    """
    Get activity aggregated by key matching a query from a site.

    The agg-by option for this command is the key to use for the aggregation and the possible options can vary depending
    on which site is being queried. For example, `--agg-by channelusername --site telegram trump` will aggregate all
    mentions of Trump on Telegram by channel. In order to better understand the available keys for aggregation, using
    the `content` tool can provide some examples.

    \f
    A Click command for the main group that makes requests to the /activity endpoint and outputs JSON results.
    """
    api = Smat()
    try:
        formatter = ctx.obj["formatter"](
            api.activity(
                term=query,
                since=since,
                until=until,
                site=site,
                agg_by=agg_by,
            )
        )
    except SmatError as e:
        click.echo("Error: " + str(e))

    for each in formatter.activity(agg_by):
        click.echo(each)


@main.command()
def sites():
    """
    Show a list of available sites.

    \f
    A Click command for the main group that outputs a list of sites available via the SMAT API.
    """
    api = Smat()
    for site in sorted(api.sites):
        click.echo(site)


if __name__ == "__main__":
    main()
