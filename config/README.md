# T001 runtime foundation

Python 3.12, one Django application with shared alpha domain/services. Web entry
points are manage.py, config.wsgi and config.asgi. Separate processes are
`python -m alpha.worker` and `python -m alpha.maintenance`; both exit 2 until
later authorized tasks supply execution and coordination. No provider SDK,
broker, request background work, signup or public media routes exist.
The health endpoint reports web liveness only, never production readiness.
SQLite durability and domain persistence are subsequent task scope.

Create a repository-local environment and install pinned dependencies from an
operator-provided offline wheel directory:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install --no-index --find-links /path/to/offline-wheels -r requirements.lock
.venv/bin/python -m unittest discover -s tests -v
```

Supply ALPHA_SECRET_KEY through the process environment using a secret manager
or operator shell: at least 50 characters, 5 distinct characters, no Django
insecure prefix. There is no source default or automatic secret-file loading.
Never print configuration/environment or put secrets in command-line arguments.
Configuration object repr and validation errors exclude secret values. Django's
standard sensitive-settings filter handles SECRET_KEY in exception reports.

ALPHA_PROFILE defaults to owner-local (loopback hosts only). invited-alpha
requires ALPHA_ALLOWED_HOSTS as comma-separated explicit hosts and enforces
HTTPS redirects and Secure cookies. Both profiles disable debug, use session/
CSRF middleware, HttpOnly/SameSite cookies and DENY framing. No forwarded proxy
headers are trusted. Configure HTTPS handling separately before invitations.
ALPHA_PROVIDERS_ENABLED defaults to false; every other value is rejected.
Unknown ALPHA_ settings fail closed. Unrelated environment keys are ignored.
No provider credentials are required or consumed.

With the externally supplied secret in the environment:

```sh
.venv/bin/python manage.py check
.venv/bin/python manage.py runserver 127.0.0.1:8000 --noreload
.venv/bin/python -m alpha.worker
.venv/bin/python -m alpha.maintenance
```

Foundation tests deny socket connection and DNS calls before importing Django
startup code, use synthetic secrets, and perform an in-process smoke request.
They require no database migration, provider credential or network access.
Existing spike/pipeline environments remain separate and are never imported.
