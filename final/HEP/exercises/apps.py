from django.apps import AppConfig


class ExercisesConfig(AppConfig):
    name = 'exercises'

    def ready(self):
        import exercises.signals