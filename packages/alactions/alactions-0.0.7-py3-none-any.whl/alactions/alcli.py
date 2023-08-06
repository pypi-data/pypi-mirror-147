import os
import click
from alactions.allib import run

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.obj is None:
        ctx.obj = {}

@cli.command(name='run')
@click.argument('pipeline')
@click.pass_context
def run_pipeline(ctx, pipeline):
    print(os.getcwd())
    run()

if __name__ == '__main__':
    cli(obj={'ok':1})