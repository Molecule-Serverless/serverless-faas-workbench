Cases from functionbench


## Known issues

This function requires Python2 to run.
However, Python2 does not have importlib.util
we should change daemon's importlib.util to:
import importlib

The above issue has been fixed


## Known requirements

- pip install chameleon
- pip install six
