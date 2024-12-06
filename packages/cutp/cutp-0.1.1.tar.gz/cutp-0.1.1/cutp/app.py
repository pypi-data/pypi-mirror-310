from random import randint

import typer
from rich import print
from typing_extensions import Annotated

from cutp.utils.ports import PORTS

app = typer.Typer(
    help='Tool to check if a given TCP port does '
    'not conflict with an Umbrel application.',
    no_args_is_help=True,
    rich_markup_mode='rich',
)


@app.command(help='Checks if the given port is available.')
def check(
    port: Annotated[
        int, typer.Argument(help='A valid TCP port between 1058 and 65535.')
    ],
):
    if port < 1058 or port > 65535:
        print(
            '[yellow bold]You must enter a port '
            'between 1058 and 65535![/yellow bold]'
        )
    elif port in PORTS:
        print(
            f'[red bold]Port {port} is already used '
            'by an Umbrel application.[/red bold]'
        )
    else:
        print(f'[green bold]Port {port} is free.[/green bold]')


@app.command(help='Suggest an available port.')
def gen():
    while True:
        port = randint(1058, 65535)

        if port not in PORTS:
            print(port)
            break
        continue  # pragma: no cover
