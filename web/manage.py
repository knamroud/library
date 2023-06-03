#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # use different settings file for production, development, and testing
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
    try:
        from library_frontend.tsccthread import TSCCThread
        from django.conf import settings
        from os.path import join
        # tscc = TSCCThread(join(settings.STATIC_ROOT, "ts"), join(
        #    settings.STATIC_ROOT, "js"), debug=settings.DEBUG)
        # tscc.start()
        execute_from_command_line(sys.argv)
    finally:
        # tscc.stop()
        pass


if __name__ == "__main__":
    main()
