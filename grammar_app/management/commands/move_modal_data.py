from django.core.management.base import BaseCommand
from grammar_app.models import GrammaticalCategory, GrammaticalForm

class Command(BaseCommand):
    help = 'Move modal data to the correct category'

    def handle(self, *args, **options):
        try:
            # Get the new Modal So'z category
            new_modal = GrammaticalCategory.objects.get(name="Modal So'z")
            
            # Find any old modal categories and move their data
            old_modals = GrammaticalCategory.objects.filter(
                name__in=["Modal so'zlar", "Modal So'z", "modal"]
            ).exclude(id=new_modal.id)
            
            # Move all forms from old categories to the new one
            for old_cat in old_modals:
                GrammaticalForm.objects.filter(category=old_cat).update(category=new_modal)
            
            self.stdout.write(self.style.SUCCESS('Successfully moved modal data to the correct category'))
            
        except GrammaticalCategory.DoesNotExist:
            self.stdout.write(self.style.ERROR('Modal So\'z category not found'))
