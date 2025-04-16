from django.core.management.base import BaseCommand
from grammar_app.models import GrammaticalCategory, GrammaticalForm

class Command(BaseCommand):
    help = 'Fix duplicate modal categories'

    def handle(self, *args, **options):
        try:
            # Get both categories
            modal_sozlar = GrammaticalCategory.objects.get(name="Modal so'zlar")
            modal_soz = GrammaticalCategory.objects.get(name="Modal So'z")

            # Move all forms from Modal So'z to Modal so'zlar
            GrammaticalForm.objects.filter(category=modal_soz).update(category=modal_sozlar)

            # Delete the Modal So'z category
            modal_soz.delete()

            # Update the order of Modal so'zlar
            modal_sozlar.order = 4
            modal_sozlar.save()

            self.stdout.write(self.style.SUCCESS('Successfully merged modal categories'))
        except GrammaticalCategory.DoesNotExist:
            self.stdout.write(self.style.ERROR('One or both categories not found'))
