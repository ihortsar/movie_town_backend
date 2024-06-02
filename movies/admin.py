from django.contrib import admin
from movies.models import Movie
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# ImportExport class exitinheritance.
class CustomMovieResource(resources.ModelResource):
    class Meta:
        model = Movie

# ImportExport class inheritance.
class MovieAdmin(ImportExportModelAdmin):
    resource_class = CustomMovieResource



admin.site.register(Movie, MovieAdmin)
