from django.apps import AppConfig


class CourseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'course'
    verbose_name = 'دوره'
    verbose_name_plural = 'دوره ها'
