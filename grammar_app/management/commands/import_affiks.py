from django.core.management.base import BaseCommand
import pandas as pd
from grammar_app.models import GrammaticalCategory, GrammaticalForm, Example

class Command(BaseCommand):
    help = "Import Affiks data from Excel file"

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        
        # Read the Excel file
        df = pd.read_excel(excel_file)
        
        # Print column names for debugging
        self.stdout.write(f"Excel columns: {list(df.columns)}")
        
        # Get Affiks category
        try:
            category = GrammaticalCategory.objects.get(name="Affiks")
            self.stdout.write(f"Found category: {category.name}")
        except GrammaticalCategory.DoesNotExist:
            category = GrammaticalCategory.objects.create(name="Affiks")
            self.stdout.write(f"Created category: {category.name}")

        # Delete existing forms to avoid duplicates
        GrammaticalForm.objects.filter(category=category).delete()
        self.stdout.write("Cleared existing Affiks data")

        # Counter for imported items
        imported_count = 0
        
        # Process each row
        for index, row in df.iterrows():
            try:
                # Create new grammatical form
                form = GrammaticalForm.objects.create(
                    category=category,
                    term=str(row['GRAMMATIK SHAKL']).strip(),
                    usage=str(row['GRAMMATIK VAZIFASI']).strip(),
                    grammatical_meaning=str(row["GRAMMATIK MA'NOLARI"]).strip(),
                    translation=str(row['TARJIMASI']).strip() if pd.notna(row['TARJIMASI']) else ''
                )

                # Create example if exists
                if pd.notna(row['MISOLLAR']):
                    Example.objects.create(
                        grammatical_form=form,
                        uzbek_text=str(row['MISOLLAR']).strip(),
                        english_translation=str(row['EXAMPLES']).strip() if pd.notna(row['EXAMPLES']) else ''
                    )

                imported_count += 1
                if imported_count % 10 == 0:
                    self.stdout.write(f"Imported {imported_count} items...")

            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(
                        f"Error importing row {index + 2} (Excel row number): {str(e)}"
                    )
                )
                continue

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully imported {imported_count} Affiks items"
            )
        ) 