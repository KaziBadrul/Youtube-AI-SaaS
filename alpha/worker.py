"""Separate production process. No scheduler or provider activation yet."""
import os
import sys
from django.core.exceptions import ImproperlyConfigured
from config.environment import load_config


def main():
    try:
        load_config(os.environ)
    except ImproperlyConfigured as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print("Production worker is unconfigured: queue admission, fencing and capability gates are not implemented.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
