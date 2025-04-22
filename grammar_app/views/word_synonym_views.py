from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
import pandas as pd
import json
from ..models import WordSynonym


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