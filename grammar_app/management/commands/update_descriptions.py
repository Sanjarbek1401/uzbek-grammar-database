from django.core.management.base import BaseCommand
from grammar_app.models import GrammaticalCategory

class Command(BaseCommand):
    help = 'Updates the descriptions of grammatical categories'

    def handle(self, *args, **kwargs):
        # Dictionary mapping category names to their new descriptions
        descriptions = {
            # Add your category names and new descriptions here
            "Yordamchi so'z": "Yordamchi so'zlar – mustaqil ma'noga ega bo'lmagan, grammatik ma'no ifodalashga xizmat qiladigan so'zlar.",
            "Ko'makchi fe'l": "Ko'makchi fe'lli so'z qo'shilmasining ko'makchi qismi",
            "Undov so'z": "Nutqiy etiket undovlari",
            
            # Add more categories and descriptions as needed
        }

        updated_count = 0
        for name, description in descriptions.items():
            try:
                category = GrammaticalCategory.objects.get(name=name)
                category.description = description
                category.save()
                self.stdout.write(self.style.SUCCESS(f'Updated description for "{name}"'))
                updated_count += 1
            except GrammaticalCategory.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Category "{name}" not found'))

        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} category descriptions')) 