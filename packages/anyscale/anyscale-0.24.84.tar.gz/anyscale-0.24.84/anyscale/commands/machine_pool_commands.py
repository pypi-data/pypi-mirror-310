"""
This file holds all of the CLI commands for the "anyscale machine-pool" path.
"""

import click
import tabulate

from anyscale.commands import command_examples
from anyscale.commands.util import AnyscaleCommand
from anyscale.controllers.machine_pool_controller import MachinePoolController


@click.group(
    "machine-pool", help="Commands to interact with machine pools in Anyscale.",
)
def machine_pool_cli() -> None:
    pass


@machine_pool_cli.command(
    name="create",
    help="Create a machine pool in Anyscale.",
    cls=AnyscaleCommand,
    example=command_examples.MACHINE_POOL_CREATE_EXAMPLE,
    is_beta=True,
)
@click.option(
    "--name",
    type=str,
    required=True,
    help="Provide a machine pool name (must be unique within an organization).",
)
@click.option(
    "--enable-rootless-dataplane-config",
    type=bool,
    default=False,
    required=False,
    help="Enable the dataplane rootless configuration for nodes running under this machine pool.",
)
def create_machine_pool(name: str, enable_rootless_dataplane_config: bool) -> None:
    machine_pool_controller = MachinePoolController()
    output = machine_pool_controller.create_machine_pool(
        machine_pool_name=name,
        enable_rootless_dataplane_config=enable_rootless_dataplane_config,
    )
    print(
        f"Machine pool {output.machine_pool.machine_pool_name} has been created successfully (ID {output.machine_pool.machine_pool_id})."
    )


@machine_pool_cli.command(
    name="delete",
    help="Delete a machine pool in Anyscale.",
    cls=AnyscaleCommand,
    example=command_examples.MACHINE_POOL_DELETE_EXAMPLE,
    is_beta=True,
)
@click.option("--name", type=str, required=True, help="Provide a machine pool name.")
def delete_machine_pool(name: str) -> None:
    machine_pool_controller = MachinePoolController()
    machine_pool_controller.delete_machine_pool(machine_pool_name=name)
    print(f"Deleted machine pool '{name}'.")


@machine_pool_cli.command(
    name="list",
    help="List machine pools in Anyscale.",
    cls=AnyscaleCommand,
    example=command_examples.MACHINE_POOL_LIST_EXAMPLE,
    is_beta=True,
)
def list_machine_pools() -> None:
    machine_pool_controller = MachinePoolController()
    output = machine_pool_controller.list_machine_pools()
    table = []
    columns = [
        "MACHINE POOL",
        "ID",
        "Clouds",
        "Rootless",
    ]
    for mp in output.machine_pools:
        table.append(
            [
                mp.machine_pool_name,
                mp.machine_pool_id,
                "\n".join(mp.cloud_ids),
                mp.enable_rootless_dataplane_config,
            ]
        )
    print(tabulate.tabulate(table, tablefmt="plain", headers=columns, stralign="left"))


@machine_pool_cli.command(name="attach", help="Attach a machine pool to a cloud.")
@click.option("--name", type=str, required=True, help="Provide a machine pool name.")
@click.option("--cloud", type=str, required=True, help="Provide a cloud name.")
def attach_machine_pool_to_cloud(name: str, cloud: str) -> None:
    machine_pool_controller = MachinePoolController()
    machine_pool_controller.attach_machine_pool_to_cloud(
        machine_pool_name=name, cloud=cloud
    )
    print(f"Attached machine pool '{name}' to cloud '{cloud}'.")


@machine_pool_cli.command(name="detach", help="Detach a machine pool from a cloud.")
@click.option("--name", type=str, required=True, help="Provide a machine pool name.")
@click.option("--cloud", type=str, required=True, help="Provide a cloud name.")
def detach_machine_pool_from_cloud(name: str, cloud: str) -> None:
    machine_pool_controller = MachinePoolController()
    machine_pool_controller.detach_machine_pool_from_cloud(
        machine_pool_name=name, cloud=cloud
    )
    print(f"Detached machine pool '{name}' from cloud '{cloud}'.")
