from django.db.models import Q
from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
import pandas as pd
import json
from ..models import GrammatikManoData


class GrammatikManoView(ListView):
    model = GrammatikManoData
    template_name = 'grammar_app/grammatik_mano.html'
    context_object_name = 'items'
    paginate_by = 20  # Show 20 items per page

    def get_queryset(self):
        queryset = super().get_queryset()
        # Add search functionality if needed
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(grammatik_manosi__icontains=q) |
                Q(badiiy_uslub__icontains=q) |
                Q(ilmiy_uslub__icontains=q) |
                Q(publitsistik_uslub__icontains=q) |
                Q(rasmiy_uslub__icontains=q) |
                Q(sozlashuv_uslubi__icontains=q)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add total count to context
        context['total_items'] = self.model.objects.count()
        # Add current page number
        context['current_page'] = self.request.GET.get('page', 1)
        # Add search query if exists
        context['search_query'] = self.request.GET.get('q', '')
        return context

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
                "So'zning grammatik ma'nosi": item.grammatik_manosi,
                "Badiiy uslub": item.badiiy_uslub,
                "Ilmiy uslub": item.ilmiy_uslub,
                "Publitsistik uslub": item.publitsistik_uslub,
                "Rasmiy uslub": item.rasmiy_uslub,
                "So'zlashuv uslubi": item.sozlashuv_uslubi,
            })
        
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="grammatik_mano_data.xlsx"'
        df.to_excel(response, index=False)
        return response

    def export_json(self, queryset):
        data = []
        for item in queryset:
            data.append({
                "grammatik_manosi": item.grammatik_manosi,
                "badiiy_uslub": item.badiiy_uslub,
                "ilmiy_uslub": item.ilmiy_uslub,
                "publitsistik_uslub": item.publitsistik_uslub,
                "rasmiy_uslub": item.rasmiy_uslub,
                "sozlashuv_uslubi": item.sozlashuv_uslubi,
            })
        
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="grammatik_mano_data.json"'
        json.dump(data, response, ensure_ascii=False, indent=2)
        return response


def import_grammatik_excel(request):
    try:
        # Read the Excel file
        df = pd.read_excel(r"C:\Users\Sanjar\Desktop\grammatik.xlsx")
        
        # Print column names for debugging
        print("Available columns:", df.columns.tolist())
        print(f"Found {len(df)} rows in the Excel file")
        
        # Clear existing data if needed
        # GrammatikManoData.objects.all().delete()
        
        # Track success and failures
        success_count = 0
        error_records = []
        
        # Process each row in the Excel file
        for index, row in df.iterrows():
            try:
                # Extract data, handling possible NaN values
                grammatik_manosi = row.get('So\'zning grammatik ma\'nosi', '')
                if pd.isna(grammatik_manosi) or not grammatik_manosi:
                    continue  # Skip rows without grammatical meaning
                
                # Create or update the record
                obj, created = GrammatikManoData.objects.update_or_create(
                    grammatik_manosi=grammatik_manosi,
                    defaults={
                        'badiiy_uslub': row.get('Badiiy uslub', '') if not pd.isna(row.get('Badiiy uslub', '')) else '',
                        'ilmiy_uslub': row.get('Ilmiy uslub', '') if not pd.isna(row.get('Ilmiy uslub', '')) else '',
                        'publitsistik_uslub': row.get('Publitsistik uslub', '') if not pd.isna(row.get('Publitsistik uslub', '')) else '',
                        'rasmiy_uslub': row.get('Rasmiy uslub', '') if not pd.isna(row.get('Rasmiy uslub', '')) else '',
                        'sozlashuv_uslubi': row.get('So\'zlashuv uslubi', '') if not pd.isna(row.get('So\'zlashuv uslubi', '')) else '',
                    }
                )
                success_count += 1
                
            except Exception as e:
                error_records.append(f"Error in row {index+2}: {str(e)}")
                print(f"Error processing row {index+2}: {str(e)}")
        
        print(f"Successfully imported {success_count} items")
        if error_records:
            print(f"Encountered {len(error_records)} errors")
            
        return JsonResponse({
            'status': 'success', 
            'message': f'Data imported successfully. {success_count} records processed.', 
            'errors': error_records
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}) 