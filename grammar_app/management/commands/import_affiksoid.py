from django.core.management.base import BaseCommand
import pandas as pd
from grammar_app.models import GrammaticalCategory, GrammaticalForm, Example

class Command(BaseCommand):
    help = "Import Affiksoid data from Excel file"

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        
        # Read the Excel file
        df = pd.read_excel(excel_file)
        df = df.fillna('')  # Replace NaN with empty string
        
        # Print column names for debugging
        self.stdout.write(f"Excel columns: {list(df.columns)}")
        
        # Get or create Affiksoid category
        try:
            category = GrammaticalCategory.objects.get(name="Affiksoid")
            self.stdout.write(f"Found category: {category.name}")
        except GrammaticalCategory.DoesNotExist:
            category = GrammaticalCategory.objects.create(name="Affiksoid")
            self.stdout.write(f"Created category: {category.name}")

        # Delete existing forms to avoid duplicates
        GrammaticalForm.objects.filter(category=category).delete()
        self.stdout.write("Cleared existing Affiksoid data")

        # Counter for imported items
        imported_count = 0
        current_term = None
        current_form = None
        
        # Process each row
        for index, row in df.iterrows():
            try:
                term = str(row['Grammatik shakl']).strip()
                
                # If this is a new term or first row
                if term and term != current_term:
                    current_term = term
                    # Create new grammatical form
                    current_form = GrammaticalForm.objects.create(
                        category=category,
                        term=term,
                        grammatical_meaning=str(row["Grammatik ma'nosi"]).strip(),
                        translation=str(row['Tarjimasi']).strip()
                    )
                    imported_count += 1
                
                # If this is a continuation of previous term
                elif current_form and not term:
                    # Append additional meaning to existing form
                    current_form.grammatical_meaning += "\n" + str(row["Grammatik ma'nosi"]).strip()
                    current_form.translation += "\n" + str(row['Tarjimasi']).strip()
                    current_form.save()

                # Create example if exists
                if row['Misollar']:
                    Example.objects.create(
                        grammatical_form=current_form,
                        uzbek_text=str(row['Misollar']).strip(),
                        english_translation=str(row['Examples in English']).strip()
                    )

                if imported_count % 10 == 0 and term:
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
                f"Successfully imported {imported_count} Affiksoid items"
            )
        ) 