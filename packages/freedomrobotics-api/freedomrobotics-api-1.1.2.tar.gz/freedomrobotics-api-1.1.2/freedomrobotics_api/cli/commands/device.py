import click

from freedomrobotics_api.cli.commands.base import (
    add_options, common_options, api_options, listing_options,
    error_message_catch, parse_list_option, parse_dict_option,
    get_freedom_client, echo_json,
)


@click.group()
def device():
    pass


@device.command()
@add_options(common_options)
@add_options(api_options)
@click.option('--id')
@click.option('--name')
def get(**kwargs):
    client = get_freedom_client(**kwargs)

    device_id = kwargs.get('id')
    device_name = kwargs.get('name')
    if not device_id and not device_name:
        raise click.UsageError("Either device --id or --name should be specified.")

    with error_message_catch("Fetch account", show_info_msg=False):
        account = client.get_account(kwargs.get('account_id'))

    with error_message_catch("Fetch device", show_info_msg=False):
        params = parse_dict_option('params', kwargs)
        if device_id:
            device_data = account.get_device(device_id, params=params, raw=True)
        elif device_name:
            devices = account.get_devices(attributes=['name'], params=params)
            for device_obj in devices:
                if device_obj.name == device_name:
                    break
            else:
                raise Exception(f"Cannot find device with name `{device_name}`")
            device_obj.update()  # retrieve all data once its found
            device_data = device_obj._data

    echo_json(device_data)


@device.command()
@add_options(common_options)
@add_options(listing_options)
@click.option('--zones', help='List of zones to filter separated by comma')
@click.option('--include-subzones',
              is_flag=True,
              help='Include also subzones in result. This will have effect only when using --zones')
def list(**kwargs):
    client = get_freedom_client(**kwargs)

    with error_message_catch("Fetch account", show_info_msg=False):
        account = client.get_account(kwargs.get('account_id'))

    attributes = parse_list_option('attributes', kwargs)
    zones = parse_list_option('zones', kwargs)
    include_subzones = parse_list_option('include_subzones', kwargs)
    params = parse_dict_option('params', kwargs)

    with error_message_catch("Fetch devices", show_info_msg=False):
        devices = account.get_devices(
            attributes=attributes,
            zones=zones,
            include_subzones=include_subzones,
            params=params,
            raw=True,
        )
    echo_json(devices)
