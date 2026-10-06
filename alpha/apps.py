from django.apps import AppConfig


class AlphaConfig(AppConfig):
    name = "alpha"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self) -> None:
        from alpha.persistence.connection import register_sqlite_pragmas

        register_sqlite_pragmas()
