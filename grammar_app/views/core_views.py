from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, TemplateView
from ..models import GrammaticalCategory, GrammaticalForm, DavriylikiData


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

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        if category.name == "Yordamchi so'z":
            return redirect('yordamchi_soz')
        elif category.name == "So'z davriyligiga ko'ra":
            # Create a dummy category for Davriylik data
            davriylik_category = GrammaticalCategory(name="So'z davriyligiga ko'ra", description="So'zning davrlar bo'yicha tarixiy o'zgarishlari")
            context = {
                'category': davriylik_category,
                'forms': DavriylikiData.objects.all(),
                'categories': GrammaticalCategory.objects.all()  # For navigation
            }
            return render(request, self.template_name, context)
        return super().get(request, *args, **kwargs)

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