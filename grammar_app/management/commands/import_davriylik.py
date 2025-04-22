import os
from django.core.management.base import BaseCommand
from django.conf import settings
import pandas as pd
from grammar_app.models import DavriylikiData
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import data from davriylik Excel file"

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='C:/Users/Sanjar/Desktop/davriyligi.xlsx',
            help='File path for the Excel file to import'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return
        
        try:
            df = pd.read_excel(file_path)
            
            # Check if required columns exist
            required_columns = ['XI-XII', 'XIII-XIV', 'XV-XVIII', 'XIX', 'XX']
            
            # Map the Excel column names to model field names
            column_mapping = {
                'XI-XII': 'period_11_12',
                'XIII-XIV': 'period_13_14',
                'XV-XVIII': 'period_15_18',
                'XIX': 'period_19',
                'XX': 'period_20'
            }
            
            # Verify all required columns exist in the file
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                self.stdout.write(self.style.ERROR(f"Missing columns in Excel file: {', '.join(missing_columns)}"))
                self.stdout.write(self.style.WARNING(f"Available columns: {', '.join(df.columns)}"))
                return
            
            # Clear existing data if needed
            # DavriylikiData.objects.all().delete()
            
            # Start importing data
            success_count = 0
            error_count = 0
            
            for _, row in df.iterrows():
                try:
                    # Extract data from the DataFrame
                    data = {}
                    for excel_col, model_field in column_mapping.items():
                        # Convert NaN values to empty string
                        value = row[excel_col]
                        if pd.isna(value):
                            value = ""
                        data[model_field] = value
                    
                    # Create a new entry with period fields only
                    obj = DavriylikiData.objects.create(**data)
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    self.stdout.write(self.style.ERROR(f"Error importing row: {str(e)}"))
            
            self.stdout.write(self.style.SUCCESS(f"Successfully imported {success_count} entries"))
            if error_count > 0:
                self.stdout.write(self.style.WARNING(f"Encountered {error_count} errors during import"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading Excel file: {str(e)}")) 