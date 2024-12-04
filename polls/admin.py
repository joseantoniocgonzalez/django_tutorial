from django.contrib import admin
from .models import Choice, Question, Categoria


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('Abr', 'Nombre', 'Cantidad')  # Mostrar estos campos en el admin
    search_fields = ('Abr', 'Nombre')  # Opcional: Hacer estos campos buscables


admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Categoria, CategoriaAdmin)
