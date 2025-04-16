from django.core.management.base import BaseCommand
import pandas as pd
from grammar_app.models import CodedWord

class Command(BaseCommand):
    help = "Import coded words from Excel file"

    def handle(self, *args, **options):
        excel_file = r"C:\Users\Sanjar\Desktop\kodlangan.xlsx"
        
        try:
            # Clear existing data
            CodedWord.objects.all().delete()
            self.stdout.write("Cleared existing coded words data")

            # Read the Excel file
            df = pd.read_excel(excel_file)
            self.stdout.write(f"Successfully read Excel file with {len(df)} rows")

            # Print column names for debugging
            self.stdout.write("Available columns: " + ", ".join(df.columns.tolist()))
            
            imported_count = 0
            
            for index, row in df.iterrows():
                try:
                    # Handle NaN values
                    def clean_value(value):
                        if pd.isna(value):
                            return ""
                        return str(value).strip()

                    # Create new CodedWord object
                    word = CodedWord.objects.create(
                        special_code=clean_value(row.get("So'zning maxsus kodi")),
                        auxiliary_word=clean_value(row.get("Yordamchi so'z")),
                        grammatical_code=clean_value(row.get("Grammatik kodi")),
                        primary_meaning=clean_value(row.get("So'zning birlamchi grammatik ma'nosi")),
                        secondary_meaning=clean_value(row.get("Ikkilamchi grammatik ma'nosi")),
                        third_meaning=clean_value(row.get("Uchinchi grammatik ma'nosi")),
                        fourth_meaning=clean_value(row.get("To'rtinchi grammatik ma'nosi")),
                        fifth_meaning=clean_value(row.get("Beshinchi grammatik ma'nosi")),
                        sixth_meaning=clean_value(row.get("Oltinchi grammatik ma'nosi")),
                        seventh_meaning=clean_value(row.get("Yettinchi grammatik ma'nosi")),
                        eighth_meaning=clean_value(row.get("Sakkizinchi grammatik ma'nosi")),
                        ninth_meaning=clean_value(row.get("To'qqizinchi grammatik ma'nosi")),
                        tenth_meaning=clean_value(row.get("O'ninchi grammatik ma'nosi"))
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
