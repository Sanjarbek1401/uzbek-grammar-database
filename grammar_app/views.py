from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.views.generic import ListView, DetailView, View, TemplateView
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
import pandas as pd
import json
from .models import GrammaticalCategory, GrammaticalForm, Example, UslubData, WordSynonym, CodedWord
from django.core.paginator import Paginator


def home(request):
    categories = GrammaticalCategory.objects.all()
    # Get a few examples from each category for the homepage
    category_examples = {}
    for category in categories:
        category_examples[category] = category.forms.all()[:5]

    context = {
        'categories': categories,
        'category_examples': category_examples,
    }
    return render(request, 'grammar_app/home.html', context)


class CategoryDetailView(DetailView):
    model = GrammaticalCategory
    template_name = 'grammar_app/category_detail.html'
    context_object_name = 'category'

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        if category.name == "Yordamchi so'z":
            return redirect('yordamchi_soz')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['forms'] = self.object.forms.all()
        return context


class FormDetailView(DetailView):
    model = GrammaticalForm
    template_name = 'grammar_app/form_detail.html'
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['examples'] = self.object.examples.all()
        return context


class SearchResultsView(ListView):
    model = GrammaticalForm
    template_name = 'grammar_app/search_results.html'
    context_object_name = 'forms'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return GrammaticalForm.objects.filter(
                Q(term__icontains=query) |
                Q(grammatical_meaning__icontains=query) |
                Q(translation__icontains=query) |
                Q(examples__uzbek_text__icontains=query) |
                Q(examples__english_translation__icontains=query)
            ).distinct()
        return GrammaticalForm.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


def export_category(request, category_id, format):
    category = get_object_or_404(GrammaticalCategory, id=category_id)
    forms = category.forms.all()
    
    if "Modal" in category.name:
        # Prepare data for Modal So'z category
        data = []
        current_meaning = None
        
        for form in forms:
            example = form.examples.first()
            row = {
                "SO'ZNING GRAMMATIK MA'NOSI": form.grammatical_meaning,
                "O'ZBEK TILIDAGI MODAL SO'ZLAR SINONIMLARI": form.term,
                "MISOLLAR": example.uzbek_text if example else "",
                "TRANSLATIONS IN ENGLISH": form.translation,
                "EXAMPLES": example.english_translation if example else ""
            }
            data.append(row)
    elif category.name == "Ko'makchi fe'l":
        # Prepare data for Ko'makchi fe'l category
        data = []
        for form in forms:
            example = form.examples.first()
            row = {
                "Ko'makchi fe'l": form.term,
                "Ma'nolari": form.grammatical_meaning,
                "Misollar": example.uzbek_text if example else "",
                "Yasalishi": form.translation,
                "Examples": example.english_translation if example else ""
            }
            data.append(row)
    elif category.name == "Affiks":
        # Prepare data for Affiks category
        data = []
        for form in forms:
            example = form.examples.first()
            row = {
                "GRAMMATIK SHAKL": form.term,
                "GRAMMATIK VAZIFASI": form.usage,
                "GRAMMATIK MA'NOLARI": form.grammatical_meaning,
                "MISOLLAR": example.uzbek_text if example else "",
                "TARJIMASI": form.translation,
                "EXAMPLES": example.english_translation if example else ""
            }
            data.append(row)
    else:
        # Prepare data for other categories
        data = []
        for form in forms:
            example = form.examples.first()
            row = {
                "Grammatik shakl": form.term,
                "Grammatik ma'nosi": form.grammatical_meaning,
                "Misollar": example.uzbek_text if example else "",
                "Tarjimasi": form.translation,
                "Examples": example.english_translation if example else ""
            }
            data.append(row)
    
    if format == 'excel':
        # Export as Excel
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{category.name}.xlsx"'
        df.to_excel(response, index=False, engine='openpyxl')
        return response
    else:
        # Export as JSON
        response = JsonResponse(data, safe=False)
        response['Content-Disposition'] = f'attachment; filename="{category.name}.json"'
        return response


def about(request):
    return render(request, 'grammar_app/about.html')


class YordamchiSozView(View):
    template_name = 'grammar_app/yordamchi_soz.html'
    
    def get(self, request):
        # Get all categories for the navigation menu
        all_categories = GrammaticalCategory.objects.all()
        
        # Get the Yordamchi so'z category
        try:
            yordamchi_category = GrammaticalCategory.objects.get(name="Yordamchi so'z")
            category_id = yordamchi_category.id
        except GrammaticalCategory.DoesNotExist:
            category_id = None

        subcategories = [
            {
                'title': 'Umumiy baza',
                'description': "Yordamchi so'zlarning to'liq bazasi",
                'url': reverse('umumiy_baza'),
            },
            {
                'title': 'Sinonimlari',
                'description': "Yordamchi so'zlarning sinonimlar to'plami",
                'url': reverse('sinonimlar'),
            },
            {
                'title': "Uslub bo'yicha saralangan",
                'description': "Uslubiy jihatdan saralangan yordamchi so'zlar",
                'url': reverse('uslub'),
            },
            {
                'title': "Grammatik ma'no bo'yicha",
                'description': "Grammatik ma'nolari bo'yicha saralangan",
                'url': '#',
            },
            {
                'title': 'Words with synonyms',
                'description': 'Sinonimik qatorlar',
                'url': reverse('word_synonyms'),
            },
            {
                'title': 'Kodlangan baza',
                'description': 'Kodlashtirilgan ma\'lumotlar bazasi',
                'url': reverse('coded_words'),
            },
            {
                'title': 'Words with examples',
                'description': 'Misollar bilan boyitilgan baza',
                'url': '#',
            },
            {
                'title': 'Tarixiylik',
                'description': 'Tarixiy jihatdan saralangan',
                'url': '#',
            },
            {
                'title': "So'zlar davriyligi",
                'description': 'Davriy jihatdan saralangan',
                'url': '#',
            },
        ]
        
        context = {
            'categories': all_categories,  # This is for the navigation menu
            'subcategories': subcategories,  # This is for the main content
            'current_category': yordamchi_category if category_id else None,
        }
        
        return render(request, self.template_name, context)


class UmumiyBazaView(View):
    template_name = 'grammar_app/umumiy_baza.html'
    
    def get(self, request):
        # Get the Yordamchi so'z category
        try:
            yordamchi_category = GrammaticalCategory.objects.get(name="Yordamchi so'z")
            forms = GrammaticalForm.objects.filter(category=yordamchi_category)
            context = {
                'forms': forms,
                'categories': GrammaticalCategory.objects.all(),  # For navigation
                'category': yordamchi_category,  # Add this line to pass category to template
            }
        except GrammaticalCategory.DoesNotExist:
            context = {
                'forms': [],
                'categories': GrammaticalCategory.objects.all(),
                'category': None
            }
        
        return render(request, self.template_name, context)


def import_yordamchi_excel(request):
    try:
        # Read the Excel file
        df = pd.read_excel(r"C:\Users\Sanjar\Desktop\Yordamchi.xlsx")
        
        # Get or create the Yordamchi so'z category
        category, _ = GrammaticalCategory.objects.get_or_create(
            name="Yordamchi so'z",
            defaults={'description': "Yordamchi so'zlar bazasi", 'order': 2}
        )
        
        # Process each row in the Excel file
        for _, row in df.iterrows():
            # Create or update the GrammaticalForm
            form, created = GrammaticalForm.objects.update_or_create(
                category=category,
                term=row['Yordamchi so\'z'],  # Adjust column name if different
                defaults={
                    'grammatical_meaning': row['Grammatik ma\'nosi'],  # Adjust column name
                    'translation': row['In English']  # Adjust column name
                }
            )
            
            # Create example if it exists
            if 'Misollar' in row and pd.notna(row['Misollar']):
                Example.objects.update_or_create(
                    grammatical_form=form,
                    defaults={
                        'uzbek_text': row['Misollar'],
                        'english_translation': row['Examples'] if pd.notna(row['Examples']) else ''
                    }
                )
        
        return JsonResponse({'status': 'success', 'message': 'Data imported successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


class SinonimlarView(View):
    template_name = 'grammar_app/sinonimlar.html'
    
    def get(self, request):
        category = GrammaticalCategory.objects.get(name="Yordamchi so'z")
        forms = GrammaticalForm.objects.filter(category=category)
        
        context = {
            'category': category,
            'forms': forms,
        }
        return render(request, self.template_name, context)


class HomeView(TemplateView):
    template_name = 'grammar_app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = GrammaticalCategory.objects.all()
        
        # Get examples from each category
        category_examples = {}
        for category in categories:
            category_examples[category] = category.forms.all()[:5]  # Get up to 5 recent forms

        context.update({
            'categories': categories,
            'category_examples': category_examples,
        })
        return context


class UslubView(ListView):
    model = UslubData
    template_name = 'grammar_app/uslub.html'
    context_object_name = 'items'

    def get(self, request, *args, **kwargs):
        if 'format' in request.GET:
            format_type = request.GET.get('format')
            queryset = self.get_queryset()
            
            if format_type == 'excel':
                return self.export_excel(queryset)
            elif format_type == 'json':
                return self.export_json(queryset)
        
        return super().get(request, *args, **kwargs)

    def export_excel(self, queryset):
        data = []
        for item in queryset:
            data.append({
                "Yordamchi so'z": item.yordamchi_soz,
                "Maxsus kodi": item.maxsus_kodi,
                "Grammatik ma'nosi": item.grammatik_manosi,
                "Badiiy": 1 if item.badiiy else 0,
                "Ilmiy": 1 if item.ilmiy else 0,
                "Publitsistik": 1 if item.publitsistik else 0,
                "Rasmiy": 1 if item.rasmiy else 0,
                "So'zlashuv": 1 if item.sozlashuv else 0,
            })
        
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="uslub_data.xlsx"'
        df.to_excel(response, index=False)
        return response

    def export_json(self, queryset):
        data = []
        for item in queryset:
            data.append({
                "yordamchi_soz": item.yordamchi_soz,
                "maxsus_kodi": item.maxsus_kodi,
                "grammatik_manosi": item.grammatik_manosi,
                "badiiy": item.badiiy,
                "ilmiy": item.ilmiy,
                "publitsistik": item.publitsistik,
                "rasmiy": item.rasmiy,
                "sozlashuv": item.sozlashuv,
            })
        
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="uslub_data.json"'
        json.dump(data, response, ensure_ascii=False, indent=2)
        return response


class WordSynonymView(ListView):
    model = WordSynonym
    template_name = 'grammar_app/word_synonyms.html'
    context_object_name = 'words'

    def get(self, request, *args, **kwargs):
        if 'format' in request.GET:
            format_type = request.GET.get('format')
            queryset = self.get_queryset()
            
            if format_type == 'excel':
                return self.export_excel(queryset)
            elif format_type == 'json':
                return self.export_json(queryset)
        
        return super().get(request, *args, **kwargs)

    def export_excel(self, queryset):
        data = []
        for item in queryset:
            data.append({
                "Grammatik so'z": item.grammatical_word,
                "Tarjimalar": item.translations,
                "Identifikator": item.identity,
                "Sinonimlar": item.synonyms,
            })
        
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="word_synonyms.xlsx"'
        df.to_excel(response, index=False)
        return response

    def export_json(self, queryset):
        data = []
        for item in queryset:
            data.append({
                "grammatical_word": item.grammatical_word,
                "translations": item.translations,
                "identity": item.identity,
                "synonyms": item.synonyms,
            })
        
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="word_synonyms.json"'
        json.dump(data, response, ensure_ascii=False, indent=2)
        return response


class CodedWordView(ListView):
    model = CodedWord
    template_name = 'grammar_app/coded_words.html'
    context_object_name = 'words'
    paginate_by = 20  # Show 20 items per page
    ordering = ['special_code']  # Order by special code

    def get(self, request, *args, **kwargs):
        if 'format' in request.GET:
            format_type = request.GET.get('format')
            queryset = self.get_queryset()
            
            if format_type == 'excel':
                return self.export_excel(queryset)
            elif format_type == 'json':
                return self.export_json(queryset)
        
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add total count to context
        context['total_items'] = self.model.objects.count()
        # Add current page number
        context['current_page'] = self.request.GET.get('page', 1)
        return context

    def export_excel(self, queryset):
        data = []
        for item in queryset:
            data.append({
                "So'zning maxsus kodi": item.special_code,
                "Yordamchi so'z": item.auxiliary_word,
                "Grammatik kodi": item.grammatical_code,
                "So'zning birlamchi grammatik ma'nosi": item.primary_meaning,
                "Ikkilamchi": item.secondary_meaning,
                "Uchinchi": item.third_meaning,
                "To'rtinchi": item.fourth_meaning,
                "Beshinchi": item.fifth_meaning,
                "Oltinchi": item.sixth_meaning,
                "Yettinchi": item.seventh_meaning,
                "Sakkizinchi": item.eighth_meaning,
                "To'qqizinchi": item.ninth_meaning,
                "O'ninchi": item.tenth_meaning,
            })
        
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="coded_words.xlsx"'
        df.to_excel(response, index=False)
        return response

    def export_json(self, queryset):
        data = []
        for item in queryset:
            data.append({
                "special_code": item.special_code,
                "auxiliary_word": item.auxiliary_word,
                "grammatical_code": item.grammatical_code,
                "primary_meaning": item.primary_meaning,
                "secondary_meaning": item.secondary_meaning,
                "third_meaning": item.third_meaning,
                "fourth_meaning": item.fourth_meaning,
                "fifth_meaning": item.fifth_meaning,
                "sixth_meaning": item.sixth_meaning,
                "seventh_meaning": item.seventh_meaning,
                "eighth_meaning": item.eighth_meaning,
                "ninth_meaning": item.ninth_meaning,
                "tenth_meaning": item.tenth_meaning,
            })
        
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="coded_words.json"'
        json.dump(data, response, ensure_ascii=False, indent=2)
        return response