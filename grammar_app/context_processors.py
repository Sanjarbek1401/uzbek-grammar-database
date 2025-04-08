from .models import GrammaticalCategory

def categories(request):
    """Add categories to every template context"""
    return {'categories': GrammaticalCategory.objects.all()}