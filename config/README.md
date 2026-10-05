# T001 runtime foundation

Python 3.12, one codebase. `config` owns Django/configuration; `alpha/models`
owns future typed ORM records, `alpha/domain` pure rules, and `alpha/services`
shared application services. No production pipeline is imported by web startup.
`/health/` is liveness only, with no data or durable work. There are no signup,
private filesystem, generation, or maintenance routes.

Reproduce dependencies in a repository-local virtual environment:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install --no-index --find-links /path/to/approved/wheelhouse -r requirements.txt
.venv/bin/python -m unittest discover -s tests/foundation -v
```

Use an operator-supplied offline wheelhouse containing the exact manifest pins.
No packages were installed for T001; verification uses the existing repository
`.venv` (Django 5.2.17). Tests use synthetic keys, isolated subprocess environment,
and deny socket connections/DNS during import, WSGI startup, checks and requests.
This command proves T001 only; categorized regression infrastructure is T003.

Configuration is loaded only from explicitly supplied environment variables.
No dotenv files, user secret files, SDKs or accounts are discovered. Supply a
private random `ALPHA_SECRET_KEY` of at least 50 characters through your process
environment; do not put its value in source, shell history or logs. Missing/weak
keys fail startup in both profiles. Configuration errors omit supplied values;
the configuration object's representation omits the key. Django DEBUG is always
false. Arbitrary request/content logging is not introduced here.

Supported variables (unknown `ALPHA_` variables fail startup):

| Variable | Behavior |
| --- | --- |
| `ALPHA_PROFILE` | `owner-local` by default, or `invited-alpha` |
| `ALPHA_SECRET_KEY` | Required private signing key; no source default |
| `ALPHA_ALLOWED_HOSTS` | Comma-separated exact hosts; local defaults are loopback only; invited profile requires explicit hosts |
| `ALPHA_PROVIDERS_ENABLED` | Defaults to `false`; any other value fails closed |

With the key supplied in the environment:

```sh
.venv/bin/python manage.py check
.venv/bin/python manage.py runserver 127.0.0.1:8000 --noreload
.venv/bin/python -m alpha.worker
.venv/bin/python -m alpha.maintenance
```

The last two commands intentionally exit 2 with a clear refusal, even with valid
web configuration: execution services, admission, fencing and maintenance
coordination are unimplemented. There is no enable switch, scheduler, broker or
provider generation authority. No database/media writes occur on these paths.

Invited configuration enforces HTTPS redirect and secure session/CSRF cookies;
both profiles retain CSRF middleware, HttpOnly/SameSite cookies, host validation
and clickjacking protection. Gateway forwarded headers are not trusted. This
profile is configuration preparation, not invitation/deployment readiness.
SQLite is configured under `private/`; persistence initialization and its durable
WAL/transaction contract belong to T002. Static files alone are public-capable;
private files are never mapped by the URL configuration. Template/static folders
are empty boundaries, not a product UI.
