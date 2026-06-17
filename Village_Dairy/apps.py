from django.apps import AppConfig


class VillageDairyConfig(AppConfig):
    name = 'Village_Dairy'

    def ready(self):
        import Village_Dairy.signals 
def ready(self):
    import Village_Dairy.signals
    