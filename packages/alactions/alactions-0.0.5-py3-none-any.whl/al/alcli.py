import click

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.obj is None:
        ctx.obj = {}


if __name__ == '__main__':
    cli(obj={'ok':1})