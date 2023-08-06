from pathlib import Path
import os

def echo(value=None, product=None, upstream=None):
    print('--')
    print(upstream)
    print('--')
    Path(product).touch()

def folder(value=None, product=None, upstream=None):
    print('--')
    print(upstream)
    print('--')
    Path(product).write_text('alactions')

def secret(secret, product=None, upstream=None):    
    print(product,"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    Path(product).write_text(secret)    