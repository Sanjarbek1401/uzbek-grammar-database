from django.shortcuts import render
from django.views.generic import TemplateView
from ..models import GrammaticalCategory


def home(request):
    categories = GrammaticalCategory.objects.all()
    # Get a few examples from each category for the homepage
    category_examples = {}
    for category in categories:
        category_examples[category] = category.forms.all()[:5]

    context = {
        'categories': categories,
        'category_examples': category_examples,
    }
    return render(request, 'grammar_app/home.html', context)


def about(request):
    return render(request, 'grammar_app/about.html')


class HomeView(TemplateView):
    template_name = 'grammar_app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = GrammaticalCategory.objects.all()
        
        # Get examples from each category
        category_examples = {}
        for category in categories:
            category_examples[category] = category.forms.all()[:5]  # Get up to 5 recent forms

        context.update({
            'categories': categories,
            'category_examples': category_examples,
        })
        return context 