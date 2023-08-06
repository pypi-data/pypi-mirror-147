from email.policy import default
import os
import sys
import click
from alactions.allib import run
import logging
from pathlib import Path

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.obj is None:
        ctx.obj = {}

@cli.command(name='run')
@click.argument('pipeline', default='pipeline.yaml')
@click.option('--target', default='.')
@click.option('--log', default='WARNING')
@click.option('--log-file')
@click.option('--env', multiple=True)
@click.option('--runs-on', default='localhost')
@click.pass_context
def run_pipeline(ctx, pipeline, target, log, log_file, env, runs_on):
    environ = {x.split('=')[0]:x.split('=')[1] for x in env}
    logFormatter = logging.Formatter('%(module)s:%(levelname)s:%(message)s')
    rootLogger = logging.getLogger()
    
    params = {}
    if log_file and Path(log_file).exists():
        Path(log_file).unlink()
        params['filename'] = log_file

        fileHandler = logging.FileHandler(log_file)
        fileHandler.setFormatter(logFormatter)
        consoleHandler.setLevel(logging.INFO)
        rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(log)
    rootLogger.addHandler(consoleHandler)
    # logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.ERROR, **params)

    # make sure we can import basic/tasks.py since basic/pipeline.yaml uses it
    # sys.path.append('basic')
    # print(os.getcwd())
    target_folder = str(Path(target).absolute())
    run(pipeline=pipeline, target_folder=target_folder, environ=environ, runs_on=runs_on)

if __name__ == '__main__':
    cli(obj={'ok':1})


#todo: run selected pipeline on a selected folder
#     