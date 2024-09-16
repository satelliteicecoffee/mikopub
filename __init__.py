'''
mikopub
LAB automatic test control module
Public version containing no specific instrument control scripts

Main contents
---
instrument                 --- instrument control scripts
utils                      --- miscellaneous functions, including logger configuration and device scanner and others
'''
import sys

from mikopub.utils.task import Task
from mikopub.utils.scan_device import scanDevice

if sys.platform.startswith("linux"):
    pass
if sys.platform.startswith("win"):
    pass


if __name__ == "__main__":
    pass

pass
