#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    if "DJANGO_SETTINGS_MODULE" not in os.environ:
        if len(sys.argv) > 1 and sys.argv[1] == "test":
            os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                                  "library.settings.test")
        elif os.environ.get("PRODUCTION", None):
            os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                                  "library.settings.production")
        else:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                                  "library.settings.development")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
