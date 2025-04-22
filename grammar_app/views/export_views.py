from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
import pandas as pd
import json
from ..models import GrammaticalCategory


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