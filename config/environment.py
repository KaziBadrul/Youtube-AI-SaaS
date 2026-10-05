"""Explicit environment-only configuration; never discover dotenv or credentials."""
import os
import re
from dataclasses import dataclass, field
from django.core.exceptions import ImproperlyConfigured


@dataclass(frozen=True)
class RuntimeConfig:
    profile: str
    secret_key: str = field(repr=False)
    allowed_hosts: tuple[str, ...]
    providers_enabled: bool = False


def load_config(environ=None):
    env = os.environ if environ is None else environ
    known = {"ALPHA_PROFILE", "ALPHA_SECRET_KEY", "ALPHA_ALLOWED_HOSTS", "ALPHA_PROVIDERS_ENABLED"}
    if any(key.startswith("ALPHA_") and key not in known for key in env):
        raise ImproperlyConfigured("Unknown ALPHA configuration setting (values withheld).")
    profile = env.get("ALPHA_PROFILE", "owner-local")
    if profile not in {"owner-local", "invited-alpha"}:
        raise ImproperlyConfigured("ALPHA_PROFILE must be owner-local or invited-alpha.")
    secret = env.get("ALPHA_SECRET_KEY", "")
    if len(secret) < 50 or len(set(secret)) < 5 or secret.startswith("django-insecure-"):
        raise ImproperlyConfigured("ALPHA_SECRET_KEY requires a private key of at least 50 characters.")
    provider_flag = env.get("ALPHA_PROVIDERS_ENABLED", "false")
    if provider_flag != "false":
        raise ImproperlyConfigured("ALPHA_PROVIDERS_ENABLED must be false; provider activation is unavailable.")
    raw_hosts = env.get("ALPHA_ALLOWED_HOSTS", "localhost,127.0.0.1,[::1]" if profile == "owner-local" else "")
    hosts = tuple(host.strip() for host in raw_hosts.split(","))
    if not hosts or any(not re.fullmatch(r"(?:[A-Za-z0-9]+(?:[.-][A-Za-z0-9]+)*|\[::1\])", host) for host in hosts):
        raise ImproperlyConfigured("ALPHA_ALLOWED_HOSTS requires explicit host names without wildcards or ports.")
    if profile == "owner-local" and not set(hosts) <= {"localhost", "127.0.0.1", "[::1]"}:
        raise ImproperlyConfigured("owner-local permits loopback hosts only.")
    return RuntimeConfig(profile, secret, hosts)
