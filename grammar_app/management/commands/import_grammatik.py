import pandas as pd
from django.core.management.base import BaseCommand
from grammar_app.models import GrammatikManoData


class Command(BaseCommand):
    help = 'Import grammatik mano data from an Excel file'

    def handle(self, *args, **kwargs):
        excel_file = r"C:\Users\Sanjar\Desktop\grammatik.xlsx"
        self.stdout.write(self.style.SUCCESS(f'Reading data from {excel_file}...'))
        
        try:
            # Read the Excel file
            df = pd.read_excel(excel_file)
            
            # Display info about the data
            self.stdout.write(self.style.SUCCESS(f'Found {len(df)} rows in the Excel file'))
            self.stdout.write(self.style.SUCCESS(f'Available columns: {df.columns.tolist()}'))
            
            # Clear existing data if needed
            # GrammatikManoData.objects.all().delete()
            # self.stdout.write(self.style.SUCCESS('Cleared existing data'))
            
            # Track success and failures
            success_count = 0
            error_count = 0
            
            # Process each row in the Excel file
            for index, row in df.iterrows():
                try:
                    # Extract data, handling possible NaN values
                    grammatik_manosi = row.get('So\'zning grammatik ma\'nosi', '')
                    if pd.isna(grammatik_manosi) or not grammatik_manosi:
                        continue  # Skip rows without grammatical meaning
                    
                    # Create or update the record
                    obj, created = GrammatikManoData.objects.update_or_create(
                        grammatik_manosi=grammatik_manosi,
                        defaults={
                            'badiiy_uslub': row.get('Badiiy uslub', '') if not pd.isna(row.get('Badiiy uslub', '')) else '',
                            'ilmiy_uslub': row.get('Ilmiy uslub', '') if not pd.isna(row.get('Ilmiy uslub', '')) else '',
                            'publitsistik_uslub': row.get('Publitsistik uslub', '') if not pd.isna(row.get('Publitsistik uslub', '')) else '',
                            'rasmiy_uslub': row.get('Rasmiy uslub', '') if not pd.isna(row.get('Rasmiy uslub', '')) else '',
                            'sozlashuv_uslubi': row.get('So\'zlashuv uslubi', '') if not pd.isna(row.get('So\'zlashuv uslubi', '')) else '',
                        }
                    )
                    success_count += 1
                    
                    if created:
                        action = "Created"
                    else:
                        action = "Updated"
                        
                    if index % 10 == 0:  # Log every 10 records
                        self.stdout.write(f"{action} record for '{grammatik_manosi[:50]}...'")
                    
                except Exception as e:
                    error_count += 1
                    self.stdout.write(self.style.ERROR(f"Error in row {index+2}: {str(e)}"))
                    
            self.stdout.write(self.style.SUCCESS(
                f'Import completed. {success_count} records processed successfully, {error_count} errors.'
            ))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to import data: {str(e)}')) 