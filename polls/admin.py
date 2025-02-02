from django.contrib import admin
from .models import Choice, Question, Categoria


# Configuración para mostrar opciones de respuesta dentro de una pregunta
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


# Configuración del modelo Question en el panel de administración
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('Abr', 'Nombre', 'Cantidad')  # Muestra estos campos en la lista del admin
    search_fields = ['Nombre', 'Abr']  # Permite buscar por nombre o abreviatura
    fields = ('Abr', 'Nombre', 'Cantidad')  # Asegúrate de incluir 'Cantidad' en el formulario de edición

# Registro de modelos en el panel de administración
admin.site.register(Question, QuestionAdmin)
admin.site.register(Categoria, CategoriaAdmin)
