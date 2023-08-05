import sys
import json
from contextlib import contextmanager

import click

from freedomrobotics_api import FreedomClient
from freedomrobotics_api.credentials import ENVIRONMENTS
from freedomrobotics_api.api_handler import MissingArgumentsError

common_options = [
    click.option('-u', '--user', help='User email'),
    click.option('--password', hide_input=True),
    click.option('--token'),
    click.option('--secret'),
    click.option('--env', '--environment', default='release', type=click.Choice(ENVIRONMENTS)),
    click.option('-a', '--account-id'),
]

listing_options = [
    click.option('--attributes', help="List of attributes to retrieve separated by comma"),
]

api_options = [
    click.option('--params', help="Key value with API query params. The format must be key=value separated by comma")
]


def add_options(options):
    """Decorator to allow sharing options between commands
    taken from https://stackoverflow.com/a/40195800/2349395
    """
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options


@contextmanager
def error_message_catch(message, show_info_msg=True, do_exit=True):
    try:
        yield
        if show_info_msg:
            click.echo(click.style(f"{message} OK", fg='green'))
    except Exception as e:
        click.echo(click.style(f"{message} FAILED: {e}", fg='red'))
        if do_exit:
            sys.exit(1)


def get_freedom_client(token=None, secret=None, user=None, password=None, url=None, env=None, **_):
    try:
        return FreedomClient(
            token=token,
            secret=secret,
            username=user,
            password=password,
            url=url,
            env=env,
        )
    except MissingArgumentsError as e:
        raise click.UsageError(str(e))


def echo_json(data):
    click.echo(json.dumps(data, indent=2))


def parse_list_option(attr_name, kwargs):
    if kwargs.get(attr_name) is None:
        return None
    return kwargs[attr_name].split(',')


def parse_dict_option(attr_name, kwargs):
    values = parse_list_option(attr_name, kwargs)
    if values is None:
        return None
    result = {}
    for value in values:
        if ':' not in value:
            raise click.UsageError(
                f"Invalid value `{value}` for {attr_name}. "
                f"Must be in a key=value format separated by comma"
            )
        key, value = values.lsplit('=', 1)
        result[key] = value
    return result
