from django.shortcuts import render
from django.views.generic import View
from django.urls import reverse
from django.http import JsonResponse
import pandas as pd
from ..models import GrammaticalCategory, GrammaticalForm, Example


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
            
        # Find the So'z davriyligiga ko'ra category ID if exists
        try:
            davriylik_category = GrammaticalCategory.objects.get(name="So'z davriyligiga ko'ra")
            davriylik_id = davriylik_category.id
        except GrammaticalCategory.DoesNotExist:
            davriylik_id = None

        subcategories = [
            {
                'name': 'Umumiy baza',
                'description': 'Yordamchi so\'z umumiy bazasi',
                'url': reverse('umumiy_baza'),
            },
            {
                'name': 'Sinonimlar',
                'description': 'Yordamchi so\'z sinonimlari',
                'url': reverse('sinonimlar'),
            },
            {
                'name': 'Uslub bo\'yicha saralangan',
                'description': 'Uslub bo\'yicha saralangan so\'zlar',
                'url': reverse('uslub'),
            },
            {
                'name': 'Words with synonyms',
                'description': 'Words with synonyms',
                'url': reverse('word_synonyms'),
            },
            {
                'name': 'Grammatik ma\'no bo\'yicha saralangan',
                'description': 'So\'zning grammatik ma\'nosi bo\'yicha saralangan',
                'url': reverse('grammatik_mano'),
            },
            {
                'name': 'So\'z davriyligiga ko\'ra',
                'description': 'So\'zning davrlar bo\'yicha tarixiy o\'zgarishlari',
                'url': reverse('category_detail', kwargs={'pk': davriylik_id}) if davriylik_id else reverse('davriylik'),
            },
        ]

        context = {
            'all_categories': all_categories,
            'category_id': category_id,
            'subcategories': subcategories,
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