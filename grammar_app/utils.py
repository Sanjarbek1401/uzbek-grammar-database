import pandas as pd
from django.core.management.base import BaseCommand
from .models import GrammaticalCategory, GrammaticalForm, Example


def import_excel_data(file_path):
    """Import data from Excel files into Django models"""

    # Create categories first
    categories = {
        'Ko\'makchi fe\'l': 'Auxiliary verbs in Uzbek',
        'Modal so\'zlar': 'Modal words in Uzbek',
        'Bog\'lama va to\'liqsiz fe\'llar': 'Linking and incomplete verbs in Uzbek',
        'Affikslar': 'Affixes in Uzbek',
    }

    for order, (name, description) in enumerate(categories.items()):
        GrammaticalCategory.objects.get_or_create(
            name=name,
            defaults={'description': description, 'order': order}
        )

    # Read Excel sheets
    try:
        df = pd.read_excel(file_path, sheet_name=None)  # Read all sheets

        for sheet_name, data in df.items():
            # Map sheet names to categories
            if 'makchi' in sheet_name.lower():
                category_name = 'Ko\'makchi fe\'l'
            elif 'modal' in sheet_name.lower():
                category_name = 'Modal so\'zlar'
            elif 'og\'lama' in sheet_name.lower() or 'to\'liqsiz' in sheet_name.lower():
                category_name = 'Bog\'lama va to\'liqsiz fe\'llar'
            elif 'affiks' in sheet_name.lower():
                category_name = 'Affikslar'
            else:
                continue  # Skip unknown sheets

            category = GrammaticalCategory.objects.get(name=category_name)

            # Process each row
            for _, row in data.iterrows():
                try:
                    # Extract fields (adjust based on your Excel structure)
                    term = row.get('Grammatik shakl') or row.iloc[0]
                    meaning = row.get('Grammatik ma\'nosi') or row.iloc[1]
                    example_uz = row.get('Misollar') or row.iloc[2]
                    translation = row.get('Tarjimasi') or row.iloc[3]
                    example_en = row.get('Examples in English') or row.iloc[4]

                    # Skip rows with empty terms
                    if pd.isna(term) or str(term).strip() == '':
                        continue

                    # Create grammatical form
                    form, created = GrammaticalForm.objects.get_or_create(
                        category=category,
                        term=str(term),
                        defaults={
                            'grammatical_meaning': str(meaning) if not pd.isna(meaning) else '',
                            'translation': str(translation) if not pd.isna(translation) else '',
                        }
                    )

                    # Create example if both fields are present
                    if not pd.isna(example_uz) and not pd.isna(example_en):
                        Example.objects.get_or_create(
                            grammatical_form=form,
                            uzbek_text=str(example_uz),
                            english_translation=str(example_en)
                        )
                except Exception as e:
                    print(f"Error processing row: {e}")
                    continue

        return True
    except Exception as e:
        print(f"Error importing data: {e}")
        return False


# Management command to import data
class Command(BaseCommand):
    help = 'Import grammar data from Excel files'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to Excel file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        success = import_excel_data(file_path)

        if success:
            self.stdout.write(self.style.SUCCESS('Successfully imported data'))
        else:
            self.stdout.write(self.style.ERROR('Failed to import data'))