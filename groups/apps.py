from django.apps import AppConfig


class GroupsConfig(AppConfig):
    name = 'groups'
    def ready(self):
        from groups import signals


