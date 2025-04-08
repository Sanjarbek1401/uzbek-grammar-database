from django.core.management.base import BaseCommand
import os
from grammar_app.utils import import_excel_data


class Command(BaseCommand):
    help = 'Import grammar data from Excel files'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to Excel file')

    def handle(self, *args, **options):
        file_path = options['file_path']

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File does not exist: {file_path}'))
            return

        self.stdout.write(self.style.SUCCESS(f'Importing data from {file_path}...'))
        success = import_excel_data(file_path)

        if success:
            self.stdout.write(self.style.SUCCESS('Successfully imported data'))
        else:
            self.stdout.write(self.style.ERROR('Failed to import data'))