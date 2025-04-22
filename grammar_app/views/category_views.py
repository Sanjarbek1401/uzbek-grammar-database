from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.http import HttpResponse, JsonResponse
import pandas as pd
from ..models import GrammaticalCategory, GrammaticalForm, DavriylikiData


class CategoryDetailView(DetailView):
    model = GrammaticalCategory
    template_name = 'grammar_app/category_detail.html'
    context_object_name = 'category'

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        if category.name == "Yordamchi so'z":
            return redirect('yordamchi_soz')
        elif category.name == "So'z davriyligiga ko'ra":
            # Create a dummy category for Davriylik data
            davriylik_category = GrammaticalCategory(name="So'z davriyligiga ko'ra", description="So'zning davrlar bo'yicha tarixiy o'zgarishlari")
            context = {
                'category': davriylik_category,
                'forms': DavriylikiData.objects.all(),
                'categories': GrammaticalCategory.objects.all()  # For navigation
            }
            return render(request, self.template_name, context)
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


def export_category(request, category_id, format):
    category = get_object_or_404(GrammaticalCategory, id=category_id)
    forms = category.forms.all()
    
    if "Modal" in category.name:
        # Prepare data for Modal So'z category
        data = []
        for form in forms:
            # Get all examples for this form
            examples = form.examples.all()
            
            # If there are no examples, create a single row with empty example fields
            if not examples:
                row = {
                    "SO'ZNING GRAMMATIK MA'NOSI": form.grammatical_meaning,
                    "O'ZBEK TILIDAGI MODAL SO'ZLAR SINONIMLARI": form.term,
                    "MISOLLAR": "",
                    "TRANSLATIONS IN ENGLISH": form.translation,
                    "EXAMPLES": ""
                }
                data.append(row)
            else:
                # For each example, create a separate row
                for example in examples:
                    row = {
                        "SO'ZNING GRAMMATIK MA'NOSI": form.grammatical_meaning,
                        "O'ZBEK TILIDAGI MODAL SO'ZLAR SINONIMLARI": form.term,
                        "MISOLLAR": example.uzbek_text,
                        "TRANSLATIONS IN ENGLISH": form.translation,
                        "EXAMPLES": example.english_translation
                    }
                    data.append(row)
    elif category.name == "Ko'makchi fe'l":
        # Prepare data for Ko'makchi fe'l category
        data = []
        for form in forms:
            # Get all examples for this form
            examples = form.examples.all()
            
            # If there are no examples, create a single row with empty example fields
            if not examples:
                row = {
                    "Ko'makchi fe'l": form.term,
                    "Ma'nolari": form.grammatical_meaning,
                    "Misollar": "",
                    "Yasalishi": form.translation,
                    "Examples": ""
                }
                data.append(row)
            else:
                # For each example, create a separate row
                for example in examples:
                    row = {
                        "Ko'makchi fe'l": form.term,
                        "Ma'nolari": form.grammatical_meaning,
                        "Misollar": example.uzbek_text,
                        "Yasalishi": form.translation,
                        "Examples": example.english_translation
                    }
                    data.append(row)
    elif category.name == "Affiks":
        # Prepare data for Affiks category
        data = []
        for form in forms:
            # Get all examples for this form
            examples = form.examples.all()
            
            # If there are no examples, create a single row with empty example fields
            if not examples:
                row = {
                    "GRAMMATIK SHAKL": form.term,
                    "GRAMMATIK VAZIFASI": form.usage,
                    "GRAMMATIK MA'NOLARI": form.grammatical_meaning,
                    "MISOLLAR": "",
                    "TARJIMASI": form.translation,
                    "EXAMPLES": ""
                }
                data.append(row)
            else:
                # For each example, create a separate row
                for example in examples:
                    row = {
                        "GRAMMATIK SHAKL": form.term,
                        "GRAMMATIK VAZIFASI": form.usage,
                        "GRAMMATIK MA'NOLARI": form.grammatical_meaning,
                        "MISOLLAR": example.uzbek_text,
                        "TARJIMASI": form.translation,
                        "EXAMPLES": example.english_translation
                    }
                    data.append(row)
    elif category.name == "Affiksoid":
        # Prepare data for Affiksoid category
        data = []
        for form in forms:
            # Get all examples for this form
            examples = form.examples.all()
            
            # If there are no examples, create a single row with empty example fields
            if not examples:
                row = {
                    "Grammatik shakl": form.term,
                    "Grammatik ma'nosi": form.grammatical_meaning,
                    "Misollar": "",
                    "Tarjimasi": form.translation,
                    "Examples": ""
                }
                data.append(row)
            else:
                # For each example, create a separate row
                for example in examples:
                    row = {
                        "Grammatik shakl": form.term,
                        "Grammatik ma'nosi": form.grammatical_meaning,
                        "Misollar": example.uzbek_text,
                        "Tarjimasi": form.translation,
                        "Examples": example.english_translation
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