from django.contrib import admin
from .models import GrammaticalCategory, GrammaticalForm, Example, UslubData, WordSynonym, GrammatikManoData, DavriylikiData, Sinonimlar

class ExampleInline(admin.TabularInline):
    model = Example
    extra = 1

@admin.register(GrammaticalCategory)
class GrammaticalCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    ordering = ('order',)
    search_fields = ('name',)

@admin.register(GrammaticalForm)
class GrammaticalFormAdmin(admin.ModelAdmin):
    list_display = ('term', 'category', 'usage', 'grammatical_meaning', 'translation')
    list_filter = ('category', 'usage')
    search_fields = ('term', 'grammatical_meaning')
    inlines = [ExampleInline]
    
    def get_fieldsets(self, request, obj=None):
        category_name = obj.category.name if obj else None
        if category_name == "Yordamchi so'z":
            return (
                (None, {
                    'fields': ('category', 'term', 'usage')
                }),
                ('Details', {
                    'fields': (
                        'grammatical_meaning',
                        'translation',
                    ),
                }),
            )
        elif category_name == "Ko'makchi fe'l":
            return (
                (None, {
                    'fields': ('category', 'term')
                }),
                ('Details', {
                    'fields': (
                        'grammatical_meaning',  # Ma'nolari
                        'translation',  # Yasalishi
                    ),
                }),
            )
        elif "Modal" in str(category_name):
            return (
                (None, {
                    'fields': ('category', 'term')
                }),
                ('Details', {
                    'fields': (
                        'grammatical_meaning',  # So'zning grammatik ma'nosi
                        'translation',  # Translations in English
                    ),
                }),
            )
        else:
            return (
                (None, {
                    'fields': ('category', 'term', 'grammatical_meaning', 'translation')
                }),
            )

    def get_list_display(self, request):
        if not request.GET.get('category__id__exact'):
            return self.list_display
            
        try:
            category = GrammaticalCategory.objects.get(id=request.GET['category__id__exact'])
            if category.name == "Ko'makchi fe'l":
                return ('term', 'grammatical_meaning', 'translation')  # term, Ma'nolari, Yasalishi
            elif "Modal" in category.name:
                return ('grammatical_meaning', 'term', 'translation')  # ma'nosi, sinonimlari, translation
        except:
            pass
            
        return self.list_display

@admin.register(UslubData)
class UslubDataAdmin(admin.ModelAdmin):
    list_display = ('yordamchi_soz', 'maxsus_kodi', 'grammatik_manosi', 
                   'badiiy', 'ilmiy', 'publitsistik', 'rasmiy', 'sozlashuv')
    list_filter = ('badiiy', 'ilmiy', 'publitsistik', 'rasmiy', 'sozlashuv')
    search_fields = ('yordamchi_soz', 'maxsus_kodi', 'grammatik_manosi')
    list_per_page = 20

    # Make the boolean fields more readable in the admin
    def badiiy(self, obj):
        return obj.badiiy
    badiiy.boolean = True
    badiiy.short_description = 'Badiiy'

    def ilmiy(self, obj):
        return obj.ilmiy
    ilmiy.boolean = True
    ilmiy.short_description = 'Ilmiy'

    def publitsistik(self, obj):
        return obj.publitsistik
    publitsistik.boolean = True
    publitsistik.short_description = 'Publitsistik'

    def rasmiy(self, obj):
        return obj.rasmiy
    rasmiy.boolean = True
    rasmiy.short_description = 'Rasmiy'

    def sozlashuv(self, obj):
        return obj.sozlashuv
    sozlashuv.boolean = True
    sozlashuv.short_description = "So'zlashuv"

@admin.register(WordSynonym)
class WordSynonymAdmin(admin.ModelAdmin):
    list_display = ('grammatical_word', 'identity', 'translations', 'synonyms')
    search_fields = ('grammatical_word', 'translations', 'identity', 'synonyms')
    list_per_page = 20

@admin.register(GrammatikManoData)
class GrammatikManoDataAdmin(admin.ModelAdmin):
    list_display = ('grammatik_manosi', 'badiiy_uslub', 'ilmiy_uslub', 
                   'publitsistik_uslub', 'rasmiy_uslub', 'sozlashuv_uslubi')
    search_fields = ('grammatik_manosi',)
    list_per_page = 20

@admin.register(DavriylikiData)
class DavriylikiDataAdmin(admin.ModelAdmin):
    list_display = ('period_11_12', 'period_13_14', 
                    'period_15_18', 'period_19', 'period_20')
    search_fields = ('period_11_12', 'period_13_14', 'period_15_18', 'period_19', 'period_20')
    list_per_page = 20

@admin.register(Sinonimlar)
class SinonimlarAdmin(admin.ModelAdmin):
    list_display = ('grammatik_manosi', 'sinonimlar', 'misol', 'english')
    search_fields = ('grammatik_manosi', 'sinonimlar')
    list_per_page = 20

admin.site.register(Example)