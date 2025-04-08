from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views.generic import ListView, DetailView
from .models import GrammaticalCategory, GrammaticalForm


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


class CategoryDetailView(DetailView):
    model = GrammaticalCategory
    template_name = 'grammar_app/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['forms'] = self.object.forms.all()
        return context


class FormDetailView(DetailView):
    model = GrammaticalForm
    template_name = 'grammar_app/form_detail.html'
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['examples'] = self.object.examples.all()
        return context


class SearchResultsView(ListView):
    model = GrammaticalForm
    template_name = 'grammar_app/search_results.html'
    context_object_name = 'forms'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return GrammaticalForm.objects.filter(
                Q(term__icontains=query) |
                Q(grammatical_meaning__icontains=query) |
                Q(translation__icontains=query) |
                Q(examples__uzbek_text__icontains=query) |
                Q(examples__english_translation__icontains=query)
            ).distinct()
        return GrammaticalForm.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


def about(request):
    return render(request, 'grammar_app/about.html')