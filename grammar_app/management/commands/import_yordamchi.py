from django.core.management.base import BaseCommand
import pandas as pd
from grammar_app.models import GrammaticalCategory, GrammaticalForm, Example
import os

class Command(BaseCommand):
    help = "Import Yordamchi so'z data from Excel file"

    def handle(self, *args, **options):
        excel_file = r"C:\Users\Sanjar\Desktop\Yordamchi.xlsx"
        
        try:
            # First, clear existing data for Yordamchi so'z category
            category = GrammaticalCategory.objects.get(name="Yordamchi so'z")
            self.stdout.write("Clearing existing data...")
            GrammaticalForm.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS("Existing data cleared successfully"))

            # Read the Excel file
            df = pd.read_excel(excel_file)
            
            # Remove duplicate rows based on YORDAMCHI SO'Z and GRAMMATIK MA'NOSI
            df = df.drop_duplicates(subset=["YORDAMCHI SO'Z", "GRAMMATIK MA'NOSI"], keep='first')
            
            self.stdout.write(f"Processing {len(df)} unique entries...")

            # Map for standardizing Turkumi values
            turkumi_map = {
                "bog'lovchi": "Bog'lovchi",
                "yuklama": "Yuklama",
                "ko'makchi": "Ko'makchi"
            }

            imported_count = 0
            
            # Process each row
            for index, row in df.iterrows():
                try:
                    # Skip empty rows
                    if pd.isna(row["YORDAMCHI SO'Z"]):
                        continue

                    # Get and standardize Turkumi value
                    turkumi = str(row["TURKUMI"]).strip().lower() if pd.notna(row["TURKUMI"]) else ""
                    standardized_turkumi = turkumi_map.get(turkumi, "")  # Get standardized value or empty string

                    # Create the grammatical form
                    form = GrammaticalForm.objects.create(
                        category=category,
                        term=str(row["YORDAMCHI SO'Z"]).strip(),
                        grammatical_meaning=str(row["GRAMMATIK MA'NOSI"]).strip() if pd.notna(row["GRAMMATIK MA'NOSI"]) else '',
                        translation=str(row["IN ENGLISH"]).strip() if pd.notna(row["IN ENGLISH"]) else '',
                        usage=standardized_turkumi  # Use standardized Turkumi value
                    )

                    # Create example if exists
                    if pd.notna(row["MISOLLAR"]) or pd.notna(row["EXAMPLES"]):
                        Example.objects.create(
                            grammatical_form=form,
                            uzbek_text=str(row["MISOLLAR"]).strip() if pd.notna(row["MISOLLAR"]) else '',
                            english_translation=str(row["EXAMPLES"]).strip() if pd.notna(row["EXAMPLES"]) else ''
                        )

                    imported_count += 1
                    if imported_count % 10 == 0:
                        self.stdout.write(f"Imported {imported_count} items...")

                    # Debug output for Turkumi
                    self.stdout.write(f"Row {index + 2}: Original Turkumi = {turkumi}, Standardized = {standardized_turkumi}")

                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Error importing row {index + 2} (Excel row number): {str(e)}\n"
                            f"Row data: {row.to_dict()}"
                        )
                    )
                    continue

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully imported {imported_count} unique Yordamchi so'z items"
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Error reading Excel file: {str(e)}"
                )
            )