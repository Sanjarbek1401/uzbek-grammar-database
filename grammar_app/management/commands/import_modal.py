from django.core.management.base import BaseCommand
import pandas as pd
import numpy as np
from grammar_app.models import GrammaticalCategory, GrammaticalForm, Example

class Command(BaseCommand):
    help = 'Import modal words from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        
        # Read the Excel file
        df = pd.read_excel(excel_file)
        
        # Get or create Modal So'z category
        category, created = GrammaticalCategory.objects.get_or_create(
            name="Modal So'z",
            defaults={
                'description': "Modal so'zlar - o'zbek tilida modal ma'no ifodalovchi so'zlar",
                'order': 4  # As per the memory, Modal So'z is 4th in order
            }
        )
        
        # Process each row in the Excel file
        current_meaning = None
        
        for idx, row in df.iterrows():
            meaning = row.get("SO'ZNING GRAMMATIK MA'NOSI")
            synonyms = row.get("O'ZBEK TILIDAGI MODAL SO'ZLAR SINONIMLARI")
            examples = row.get("MISOLLAR")
            translations = row.get("TRANSLATIONS IN ENGLISH")
            eng_examples = row.get("EXAMPLES")
            
            # Skip if all main columns are empty
            if pd.isna(meaning) and pd.isna(synonyms) and pd.isna(examples) and pd.isna(translations):
                continue
                
            # If we have a meaning, start a new group
            if pd.notna(meaning):
                current_meaning = str(meaning).strip()
            
            # Process synonyms if present
            if pd.notna(synonyms):
                # Create a new grammatical form or update existing one
                form, created = GrammaticalForm.objects.update_or_create(
                    category=category,
                    term=str(synonyms).strip(),
                    defaults={
                        'grammatical_meaning': current_meaning or '',
                        'translation': str(translations).strip() if pd.notna(translations) else ''
                    }
                )
                
                # Create or update examples if present
                if pd.notna(examples) or pd.notna(eng_examples):
                    Example.objects.update_or_create(
                        grammatical_form=form,
                        defaults={
                            'uzbek_text': str(examples).strip() if pd.notna(examples) else '',
                            'english_translation': str(eng_examples).strip() if pd.notna(eng_examples) else ''
                        }
                    )
                
        self.stdout.write(self.style.SUCCESS('Successfully imported modal words'))
