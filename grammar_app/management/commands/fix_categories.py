from django.core.management.base import BaseCommand
from grammar_app.models import GrammaticalCategory

class Command(BaseCommand):
    help = 'Fix all categories and their order'

    def handle(self, *args, **options):
        # Define the correct categories and their order
        categories = [
            {"name": "Affiks", "order": 1},
            {"name": "Yordamchi so'z", "order": 2},
            {"name": "Undov so'z", "order": 3},
            {"name": "Modal So'z", "order": 4},
            {"name": "Affiksoid", "order": 5},
            {"name": "Ko'makchi fe'l", "order": 6},
            
        ]

        # Clear existing categories that don't match our list
        existing_names = [cat["name"] for cat in categories]
        GrammaticalCategory.objects.exclude(name__in=existing_names).delete()

        # Create or update each category
        for cat in categories:
            GrammaticalCategory.objects.update_or_create(
                name=cat["name"],
                defaults={
                    "order": cat["order"],
                    "description": f"{cat['name']} - o'zbek tilidagi {cat['name'].lower()}"
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully fixed all categories'))
