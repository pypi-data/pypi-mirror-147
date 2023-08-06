from pathlib import Path
import logging
import os
import shutil
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def echo(value=None, product=None, upstream=None):
    if value is None:
        Path(product).touch()    
    else:
        if value.startswith('$'):
            value = value[1:]
        Path(product).write_text(value)

def copy(source, target, product=None, upstream=None):
    print(source,target)
    if source.startswith('$'):
        source = source[1:]
    if target.startswith('$'):
        target = target[1:]

    source_path = Path(source)
    target_path = Path(target)
    if target_path.exists():
        raise Exception(f'target exists: {target_path}')

    shutil.copy(source_path, target_path)
    Path(product).write_text(str(target_path))

def folder(value=None, product=None, upstream=None):
    folder = Path('.').absolute().name
    Path(product).write_text(folder)



def secret(secret, product=None, upstream=None):      
    if secret.startswith('$'):
        secret = secret[1:]

    Path(product).write_text(secret)    