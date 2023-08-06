from pathlib import Path
import logging
import os
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def echo(value=None, product=None, upstream=None):
    Path(product).touch()

def folder(value=None, product=None, upstream=None):
    Path(product).write_text('alactions')

def secret(secret, product=None, upstream=None):      
    if secret.startswith('$'):
        secret = secret[1:]

    Path(product).write_text(secret)    