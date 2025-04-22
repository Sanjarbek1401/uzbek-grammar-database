from django.db.models import Q
from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
import pandas as pd
import json
from ..models import DavriylikiData


class DavriylikiView(ListView):
    model = DavriylikiData
    template_name = 'grammar_app/davriylik.html'
    context_object_name = 'items'
    paginate_by = 70  # Show 70 items per page

    def get_queryset(self):
        queryset = super().get_queryset()
        # Add search functionality
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(period_11_12__icontains=q) |
                Q(period_13_14__icontains=q) |
                Q(period_15_18__icontains=q) |
                Q(period_19__icontains=q) |
                Q(period_20__icontains=q)
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
                "XI-XII asrlar": item.period_11_12,
                "XIII-XIV asrlar": item.period_13_14,
                "XV-XVIII asrlar": item.period_15_18,
                "XIX asr": item.period_19,
                "XX asr": item.period_20,
            })
        
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="davriylik_data.xlsx"'
        df.to_excel(response, index=False)
        return response

    def export_json(self, queryset):
        data = []
        for item in queryset:
            data.append({
                "period_11_12": item.period_11_12,
                "period_13_14": item.period_13_14,
                "period_15_18": item.period_15_18,
                "period_19": item.period_19,
                "period_20": item.period_20,
            })
        
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="davriylik_data.json"'
        json.dump(data, response, ensure_ascii=False, indent=2)
        return response


def import_davriylik_excel(request):
    try:
        # Read the Excel file
        df = pd.read_excel(r"C:\Users\Sanjar\Desktop\davriyligi.xlsx")
        
        # Print column names for debugging
        print("Available columns:", df.columns.tolist())
        print(f"Found {len(df)} rows in the Excel file")
        
        # Clear existing data if needed
        # DavriylikiData.objects.all().delete()
        
        # Track success and failures
        success_count = 0
        error_records = []
        
        # Process each row in the Excel file
        for index, row in df.iterrows():
            try:
                # Create a new record directly with period fields
                obj = DavriylikiData.objects.create(
                    period_11_12=row.get('XI-XII', '') if not pd.isna(row.get('XI-XII', '')) else '',
                    period_13_14=row.get('XIII-XIV', '') if not pd.isna(row.get('XIII-XIV', '')) else '',
                    period_15_18=row.get('XV-XVIII', '') if not pd.isna(row.get('XV-XVIII', '')) else '',
                    period_19=row.get('XIX', '') if not pd.isna(row.get('XIX', '')) else '',
                    period_20=row.get('XX', '') if not pd.isna(row.get('XX', '')) else '',
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