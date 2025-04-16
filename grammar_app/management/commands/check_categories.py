from django.core.management.base import BaseCommand
from grammar_app.models import GrammaticalCategory

class Command(BaseCommand):
    help = 'Check existing categories'

    def handle(self, *args, **options):
        categories = GrammaticalCategory.objects.all()
        self.stdout.write("Existing categories:")
        for category in categories:
            self.stdout.write(f"ID: {category.id}, Name: {category.name}, Order: {category.order}")
