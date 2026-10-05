"""Fail-closed process foundation, with no scheduler or execution authority."""
import sys
from config.environment import load_config
from django.core.exceptions import ImproperlyConfigured


def refuse_unconfigured_execution(role):
    try:
        load_config()
    except ImproperlyConfigured as error:
        print(f"{role}: configuration rejected: {error}", file=sys.stderr)
        return 2
    print(f"{role}: execution unavailable; required runtime services and coordination are not configured.", file=sys.stderr)
    return 2
