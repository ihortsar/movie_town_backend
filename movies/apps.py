from django.apps import AppConfig

class MoviesConfig(AppConfig):
    """
    Configuration class for the 'movies' application.

    This class is used to configure application-specific settings for the 'movies' app,
    including setting up any necessary signal handlers when the application starts.

    Attributes:
        default_auto_field (str): The type of auto-generated primary key to use for models.
        name (str): The name of the application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'

    def ready(self):
        """
        Override this method to perform initialization tasks when the application is ready.
        
        Specifically, this method imports the signals module to ensure that any signal handlers
        defined there are connected to the appropriate signals. This is important for ensuring
        that the application's signal processing logic is executed correctly.

        Signals are used to perform actions automatically in response to certain events,
        such as saving a model instance or creating a new record.
        """
        from . import signals  
