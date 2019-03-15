#!/usr/bin/env python
import os
import sys

from the_mechanic_backend.env_dir.base import set_environment

if __name__ == '__main__':
    set_environment()
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
