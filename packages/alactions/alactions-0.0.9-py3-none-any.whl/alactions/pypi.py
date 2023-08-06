#%%
import json
import requests
from distutils.version import StrictVersion
from pathlib import Path

def versions(package_name):
    data = requests.get(f"https://pypi.org/pypi/{package_name}/json").json()
    versions = data["releases"].keys()
    valid_versions = []
    for v in versions:
        try:
            vv = StrictVersion(v)
            valid_versions.append(v)
        except:
            pass

    valid_versions.sort(key=StrictVersion)    
    return valid_versions
    
def next_version(package=None, product=None, upstream=None):
    if package is None:
        k, = upstream.to_dict()
        package = Path(str(upstream[k])).read_text()

    try:
        last_version = versions(package)[-1]
        parts = last_version.split('.')
        parts[-1] = str(int(parts[-1]) + 1)
        nv = '.'.join(parts)
    except:
        nv = '0.0.1'

    Path(product).write_text(nv)
    return nv

        
if __name__ == '__main__':
    print("\n".join(versions("scikit-image")))