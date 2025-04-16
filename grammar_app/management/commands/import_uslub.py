from django.core.management.base import BaseCommand
import pandas as pd
from grammar_app.models import UslubData
import os

class Command(BaseCommand):
    help = "Import uslub data from Excel file"

    def handle(self, *args, **options):
        excel_file = r"C:\Users\Sanjar\Desktop\uslub.xlsx"
        
        try:
            # Read the Excel file
            df = pd.read_excel(excel_file)
            
            # Clean column names by removing trailing spaces
            df.columns = df.columns.str.strip()
            
            # Clear existing data
            UslubData.objects.all().delete()
            self.stdout.write("Cleared existing uslub data")
            
            imported_count = 0
            
            for index, row in df.iterrows():
                try:
                    def convert_to_bool(value):
                        if pd.isna(value):
                            return False
                        if isinstance(value, str):
                            # If it's text data, return False
                            if any(c.isalpha() for c in value):
                                return False
                            value = value.strip()
                        try:
                            return bool(int(float(str(value))))
                        except (ValueError, TypeError):
                            return False

                    # Create the UslubData object
                    uslub = UslubData.objects.create(
                        yordamchi_soz=str(row.get("Yordamchi so'z", "")).strip(),
                        maxsus_kodi=str(row.get("Maxsus kodi", "")).strip(),
                        grammatik_manosi=str(row.get("Grammatik ma'nosi", "")).strip(),
                        badiiy=convert_to_bool(row.get("Badiiy")),  # Remove space
                        ilmiy=convert_to_bool(row.get("Ilmiy")),    # Remove space
                        publitsistik=convert_to_bool(row.get("Publitsistik")),
                        rasmiy=convert_to_bool(row.get("Rasmiy")),
                        sozlashuv=convert_to_bool(row.get("So'zlashuv"))
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
