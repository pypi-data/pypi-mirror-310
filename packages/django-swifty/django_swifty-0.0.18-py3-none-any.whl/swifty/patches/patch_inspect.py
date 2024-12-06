"""
This module provides a monkey patch for the inspect module to replace
the deprecated getargspec function with a compatible alternative using
signature.
"""

import inspect


# Monkey patch getargspec to use signature instead
# Save the original getargspec function
original_getargspec = inspect.getargspec


# Create a replacement function
def patched_getargspec(func):
    """Return the argument specification of a callable."""
    # Use inspect.signature instead of getargspec
    signature = inspect.signature(func)
    # Mimic the output structure of getargspec
    args = list(signature.parameters.values())
    return args, {}, {}  # Return a tuple similar to getargspec's return value


# Apply the monkey patch
inspect.getargspec = patched_getargspec
print("Monkey patch applied: getargspec is now using signature.")
