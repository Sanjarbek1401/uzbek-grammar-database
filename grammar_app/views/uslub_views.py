from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
import pandas as pd
import json
from ..models import UslubData


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