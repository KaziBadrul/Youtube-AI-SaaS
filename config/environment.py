"""Strict configuration; no secret-file discovery or provider initialization."""
from collections.abc import Mapping
from dataclasses import dataclass, field

from django.core.exceptions import ImproperlyConfigured


@dataclass(frozen=True)
class RuntimeConfig:
    profile: str
    secret_key: str = field(repr=False)
    allowed_hosts: tuple[str, ...]
    providers_enabled: bool = False


def load_config(env: Mapping[str, str]) -> RuntimeConfig:
    known = {"ALPHA_PROFILE", "ALPHA_SECRET_KEY", "ALPHA_ALLOWED_HOSTS", "ALPHA_PROVIDERS_ENABLED"}
    if any(key.startswith("ALPHA_") and key not in known for key in env):
        raise ImproperlyConfigured("Unknown ALPHA setting; consult config/README.md.")
    profile = env.get("ALPHA_PROFILE", "owner-local")
    if profile not in {"owner-local", "invited-alpha"}:
        raise ImproperlyConfigured("Invalid ALPHA_PROFILE.")
    secret = env.get("ALPHA_SECRET_KEY", "")
    if len(secret) < 50 or len(set(secret)) < 5 or secret.startswith("django-insecure-"):
        raise ImproperlyConfigured("ALPHA_SECRET_KEY requires a strong externally supplied secret of at least 50 characters.")
    if env.get("ALPHA_PROVIDERS_ENABLED", "false") != "false":
        raise ImproperlyConfigured("Provider execution is unavailable; ALPHA_PROVIDERS_ENABLED must be false.")
    default_hosts = "localhost,127.0.0.1,[::1]" if profile == "owner-local" else ""
    hosts = tuple(part.strip() for part in env.get("ALPHA_ALLOWED_HOSTS", default_hosts).split(",") if part.strip())
    if not hosts or any("*" in host or "/" in host for host in hosts):
        raise ImproperlyConfigured("ALPHA_ALLOWED_HOSTS requires explicit host names.")
    if profile == "owner-local" and any(host not in {"localhost", "127.0.0.1", "[::1]"} for host in hosts):
        raise ImproperlyConfigured("owner-local hosts must be loopback; use invited-alpha for private HTTPS access.")
    return RuntimeConfig(profile, secret, hosts)
