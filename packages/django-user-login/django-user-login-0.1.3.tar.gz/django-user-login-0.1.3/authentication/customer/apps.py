from django.apps import AppConfig


class CustomerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication.customer'


    def ready(self):
        import authentication.customer.signals
