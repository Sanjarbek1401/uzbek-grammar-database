from django.db.models import Q
from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
import pandas as pd
import json
from ..models import Sinonimlar, GrammaticalCategory


class SinonimlarView(ListView):
    model = Sinonimlar
    template_name = 'grammar_app/sinonimlar.html'
    context_object_name = 'sinonimlar'
    paginate_by = 48  # Show 48 items per page
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Add search functionality
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(grammatik_manosi__icontains=q) |
                Q(sinonimlar__icontains=q) |
                Q(misol__icontains=q) |
                Q(english__icontains=q)
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
        
        # Get the Yordamchi so'z category for navigation links
        try:
            context['category'] = GrammaticalCategory.objects.get(name="Yordamchi so'z")
        except GrammaticalCategory.DoesNotExist:
            context['category'] = None
            
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
                "SO'ZNING GRAMMATIK MA'NOSI": item.grammatik_manosi,
                "SINONIMLAR": item.sinonimlar,
                "MISOL": item.misol,
                "IN ENGLISH": item.english
            })
        
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="sinonimlar.xlsx"'
        df.to_excel(response, index=False)
        return response
    
    def export_json(self, queryset):
        data = []
        for item in queryset:
            data.append({
                "grammatik_manosi": item.grammatik_manosi,
                "sinonimlar": item.sinonimlar,
                "misol": item.misol,
                "english": item.english
            })
        
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="sinonimlar.json"'
        json.dump(data, response, ensure_ascii=False, indent=2)
        return response


def import_sinonimlar_excel(request):
    try:
        # Read the Excel file
        df = pd.read_excel(r"C:\Users\Sanjar\Desktop\Sinonimlari.xlsx")
        
        # Print column names for debugging
        print("Available columns:", df.columns.tolist())
        print(f"Found {len(df)} rows in the Excel file")
        
        # Clear existing data if needed
        Sinonimlar.objects.all().delete()
        
        # Track success and failures
        success_count = 0
        error_records = []
        
        # Process each row in the Excel file
        for index, row in df.iterrows():
            try:
                # Extract data, handling possible NaN values
                grammatik_manosi = row.get("SO'ZNING GRAMMATIK MA'NOSI", "")
                sinonimlar = row.get("SINONIMLAR", "")
                
                if pd.isna(grammatik_manosi) or pd.isna(sinonimlar) or not grammatik_manosi or not sinonimlar:
                    continue  # Skip rows without main data
                
                # Create the record
                Sinonimlar.objects.create(
                    grammatik_manosi=grammatik_manosi,
                    sinonimlar=sinonimlar,
                    misol=row.get("MISOL", "") if not pd.isna(row.get("MISOL", "")) else "",
                    english=row.get("IN ENGLISH", "") if not pd.isna(row.get("IN ENGLISH", "")) else ""
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