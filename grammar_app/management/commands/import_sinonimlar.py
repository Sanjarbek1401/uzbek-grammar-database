from django.core.management.base import BaseCommand
import pandas as pd
from grammar_app.models import Sinonimlar
import os

class Command(BaseCommand):
    help = "Import sinonimlar data from Excel file"

    def add_arguments(self, parser):
        parser.add_argument(
            '--file', 
            type=str,
            default='C:/Users/Sanjar/Desktop/Sinonimlari.xlsx',
            help='Path to the Excel file containing synonym data'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return
            
        try:
            # Read the Excel file
            df = pd.read_excel(file_path)
            
            # Print columns for debugging
            self.stdout.write(f"Excel columns: {list(df.columns)}")
            self.stdout.write(f"Found {len(df)} rows in the Excel file")
            
            # Clear existing data
            Sinonimlar.objects.all().delete()
            self.stdout.write("Cleared existing sinonimlar data")
            
            # Import count
            success_count = 0
            error_count = 0
            
            # Actual column names from the Excel file (based on the output)
            grammatik_column = "So'zning grammatik ma'nosi"
            sinonimlar_column = "Sinonimlar"
            misol_column = "Misol"
            english_column = "      In English"  # Note the extra spaces
            
            # Check if columns exist
            missing_columns = []
            for col in [grammatik_column, sinonimlar_column]:
                if col not in df.columns:
                    missing_columns.append(col)
                    
            if missing_columns:
                self.stdout.write(self.style.ERROR(f"Missing required columns: {missing_columns}"))
                self.stdout.write(self.style.WARNING(f"Available columns: {list(df.columns)}"))
                return
            
            # Process each row
            for _, row in df.iterrows():
                try:
                    # Extract data
                    grammatik_manosi = row.get(grammatik_column, "")
                    sinonimlar = row.get(sinonimlar_column, "")
                    
                    # Skip rows with empty main fields
                    if pd.isna(grammatik_manosi) or pd.isna(sinonimlar) or not grammatik_manosi or not sinonimlar:
                        self.stdout.write(self.style.WARNING(f"Skipping row with empty grammatik_manosi or sinonimlar"))
                        continue
                    
                    # Get misol and english if columns exist
                    misol = ""
                    if misol_column in df.columns and not pd.isna(row.get(misol_column, "")):
                        misol = row.get(misol_column, "")
                        
                    english = ""
                    if english_column in df.columns and not pd.isna(row.get(english_column, "")):
                        english = row.get(english_column, "")
                    
                    # Create the object
                    Sinonimlar.objects.create(
                        grammatik_manosi=grammatik_manosi,
                        sinonimlar=sinonimlar,
                        misol=misol,
                        english=english
                    )
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    self.stdout.write(self.style.ERROR(f"Error importing row: {e}"))
            
            self.stdout.write(self.style.SUCCESS(f"Successfully imported {success_count} items"))
            if error_count > 0:
                self.stdout.write(self.style.WARNING(f"Encountered {error_count} errors during import"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading Excel file: {e}")) 