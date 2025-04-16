from django.core.management.base import BaseCommand
import pandas as pd
import numpy as np
from grammar_app.models import GrammaticalCategory, GrammaticalForm, Example

class Command(BaseCommand):
    help = "Import Ko'makchi fe'l data from Excel file"

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        
        # Read the Excel file
        df = pd.read_excel(excel_file)
        
        # Print column names for debugging
        self.stdout.write(f"Excel columns: {list(df.columns)}")
        
        # Get or create Ko'makchi fe'l category
        try:
            category = GrammaticalCategory.objects.get(name="Ko'makchi fe'l")
            self.stdout.write(f"Found category: {category.name}")
        except GrammaticalCategory.DoesNotExist:
            category = GrammaticalCategory.objects.create(name="Ko'makchi fe'l")
            self.stdout.write(f"Created category: {category.name}")

        # Delete existing forms to avoid duplicates
        GrammaticalForm.objects.filter(category=category).delete()
        self.stdout.write("Cleared existing Ko'makchi fe'l data")

        # Counter for imported items
        imported_count = 0
        current_form = None
        
        # Process each row
        for index, row in df.iterrows():
            try:
                term = str(row["Ko'makchi fe'l"]).strip()
                meaning = str(row["Ma'nolari"]).strip() if not pd.isna(row["Ma'nolari"]) else ''
                example_uz = str(row["Misollar"]).strip() if not pd.isna(row["Misollar"]) else ''
                yasalishi = str(row["Yasalishi "]).strip() if not pd.isna(row["Yasalishi "]) else ''
                example_en = str(row["Examples"]).strip() if not pd.isna(row["Examples"]) else ''

                # Skip completely empty rows
                if not any([term, meaning, example_uz, yasalishi, example_en]):
                    continue
                
                # If this is a new term (not NaN in first column)
                if not pd.isna(row["Ko'makchi fe'l"]):
                    # Save previous form if exists
                    if current_form:
                        current_form.save()
                    
                    # Create new grammatical form
                    current_form = GrammaticalForm.objects.create(
                        category=category,
                        term=term,
                        grammatical_meaning=meaning,
                        translation=yasalishi
                    )
                    imported_count += 1
                    
                    # Create example if exists
                    if example_uz or example_en:
                        Example.objects.create(
                            grammatical_form=current_form,
                            uzbek_text=example_uz,
                            english_translation=example_en
                        )
                
                # If this is an additional meaning/example for the current term
                elif current_form and (meaning or example_uz or example_en or yasalishi):
                    # Add new meanings
                    if meaning:
                        if current_form.grammatical_meaning:
                            current_form.grammatical_meaning += "\n"
                        current_form.grammatical_meaning += meaning
                    
                    # Add new yasalishi
                    if yasalishi:
                        if current_form.translation:
                            current_form.translation += "\n"
                        current_form.translation += yasalishi
                    
                    current_form.save()
                    
                    # Create additional example if exists
                    if example_uz or example_en:
                        Example.objects.create(
                            grammatical_form=current_form,
                            uzbek_text=example_uz,
                            english_translation=example_en
                        )

                if imported_count % 10 == 0 and not pd.isna(row["Ko'makchi fe'l"]):
                    self.stdout.write(f"Imported {imported_count} items...")

            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(
                        f"Error importing row {index + 2} (Excel row number): {str(e)}"
                    )
                )
                continue

        # Save the last form if exists
        if current_form:
            current_form.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully imported {imported_count} Ko'makchi fe'l items"
            )
        )
