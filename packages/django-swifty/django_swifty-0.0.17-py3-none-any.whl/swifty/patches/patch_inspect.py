"""
This module provides a monkey patch for the inspect module to replace
the deprecated getargspec function with a compatible alternative using
signature.
"""

import inspect


# Monkey patch getargspec to use signature instead
def getargspec_compat(func):
    """Return the parameters of a function as a mapping."""
    return inspect.signature(func).parameters


# Replace the usage of getargspec in the library
inspect.getargspec = getargspec_compat
