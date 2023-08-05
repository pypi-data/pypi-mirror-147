__requires__ = ["numpy>=1.16,<1.20"]  # C_API_VERSION 0x0d (numpy.core.setup_common.py)
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict
try:
    pkg_resources.require(__requires__)
    numpy_dist = pkg_resources.get_distribution("numpy")
except VersionConflict:
    version = pkg_resources.get_distribution("numpy").version
    raise ModuleNotFoundError(f"pyftc needs {__requires__}, but {version} is installed!")
except DistributionNotFound:
    raise ModuleNotFoundError(f"pyftc needs numpy installed!")
from .pyftc import *

if 0:
    from numpy.core import setup_common
    from numpy import __version__ as numpy_version
    print(f"numpy {numpy_version} (C_API_VERSION: 0x{setup_common.C_API_VERSION:02x}, C_ABI_VERSION: 0x{setup_common.C_ABI_VERSION:x})")