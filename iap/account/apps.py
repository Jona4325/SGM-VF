from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    # Desactivamos temporalmente el método ready para tomar el control manual
    # def ready(self):
    #     import account.admin  # noqa: F401
