from django.contrib import admin
from . import models

admin.site.register(models.Parameter)
admin.site.register(models.Country)
admin.site.register(models.CountryParameter)
admin.site.register(models.Championship)
admin.site.register(models.Round)
admin.site.register(models.Match)

# Register your models here.
