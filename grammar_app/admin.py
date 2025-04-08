from django.contrib import admin
from .models import GrammaticalCategory, GrammaticalForm, Example

class ExampleInline(admin.TabularInline):
    model = Example
    extra = 1

class GrammaticalFormAdmin(admin.ModelAdmin):
    list_display = ('term', 'category', 'translation')
    list_filter = ('category', 'period', 'style')
    search_fields = ('term', 'grammatical_meaning', 'translation')
    inlines = [ExampleInline]

class GrammaticalCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    search_fields = ('name', 'description')

admin.site.register(GrammaticalCategory, GrammaticalCategoryAdmin)
admin.site.register(GrammaticalForm, GrammaticalFormAdmin)
admin.site.register(Example)