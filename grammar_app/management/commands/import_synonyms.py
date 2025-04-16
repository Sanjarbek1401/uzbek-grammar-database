from django.core.management.base import BaseCommand
import pandas as pd
from grammar_app.models import WordSynonym

class Command(BaseCommand):
    help = "Import word synonyms from Excel file"

    def handle(self, *args, **options):
        excel_file = r"C:\Users\Sanjar\Desktop\sinonim.xlsx"
        
        try:
            # Clear existing data
            WordSynonym.objects.all().delete()
            self.stdout.write("Cleared existing word synonyms data")

            # Read the Excel file
            df = pd.read_excel(excel_file)
            
            # Debug: Print the column names from Excel
            self.stdout.write("Excel columns found: " + ", ".join(df.columns.tolist()))
            self.stdout.write(f"Number of rows in Excel: {len(df)}")

            # Debug: Print first row of data
            if len(df) > 0:
                self.stdout.write("First row data:")
                self.stdout.write(str(df.iloc[0].to_dict()))
            
            imported_count = 0
            
            for index, row in df.iterrows():
                try:
                    # Debug: Print each row being processed
                    self.stdout.write(f"\nProcessing row {index + 2}:")
                    for col in df.columns:
                        self.stdout.write(f"{col}: {row[col]}")

                    # Handle NaN values and convert to string
                    grammatical_word = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ""
                    translations = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ""
                    identity = str(row.iloc[2]) if pd.notna(row.iloc[2]) else ""
                    synonyms = str(row.iloc[3]) if pd.notna(row.iloc[3]) else ""

                    # Create new WordSynonym object
                    word = WordSynonym.objects.create(
                        grammatical_word=grammatical_word.strip(),
                        translations=translations.strip(),
                        identity=identity.strip(),
                        synonyms=synonyms.strip()
                    )

                    imported_count += 1
                    if imported_count % 10 == 0:
                        self.stdout.write(f"Imported {imported_count} items...")

                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Error importing row {index + 2}: {str(e)}\n"
                            f"Row data: {row.to_dict()}"
                        )
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully imported {imported_count} items"
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Error: {str(e)}"
                )
            )
