from pathlib import Path

def echo(value, product=None, upstream=None):
    print('--')
    print(upstream)
    print('--')
    Path(product).touch()