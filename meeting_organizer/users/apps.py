from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'  # Pełna ścieżka Pythona do aplikacji
  
    def ready(self):
        import users.signals
