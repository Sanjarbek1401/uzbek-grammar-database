from django.db.models import Q
from django.views.generic import ListView
from django.urls import reverse
from ..models import GrammaticalForm, UslubData, WordSynonym, GrammatikManoData, Sinonimlar


class SearchResultsView(ListView):
    template_name = 'grammar_app/search_results.html'
    context_object_name = 'results'
    paginate_by = 20

    def normalize_uzbek_chars(self, text):
        """
        Normalize Uzbek special characters to ensure consistent searching
        Converts both standard Latin (o', g') and Unicode (oʻ, gʻ) to a consistent form
        """
        if not text:
            return text
            
        # First convert Unicode back to standard form for normalization
        text = text.replace("oʻ", "o'").replace("gʻ", "g'")
        return text
        
    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        if not query:
            return []
            
        # Normalize the search query to handle Uzbek special characters
        original_query = query
        normalized_query = self.normalize_uzbek_chars(query)
        
        # Create a list of queries to search for (both original and normalized)
        queries = [original_query]
        if normalized_query != original_query:
            queries.append(normalized_query)
            
        # Create Q objects for different versions of the query
        form_q = Q()
        uslub_q = Q()
        synonym_q = Q()
        
        for q in queries:
            # Search in GrammaticalForm
            form_q |= (
                Q(term__icontains=q) |
                Q(grammatical_meaning__icontains=q) |
                Q(translation__icontains=q) |
                Q(special_code__icontains=q) |
                Q(examples__uzbek_text__icontains=q) |
                Q(examples__english_translation__icontains=q)
            )
            
            # Search in UslubData
            uslub_q |= (
                Q(yordamchi_soz__icontains=q) |
                Q(maxsus_kodi__icontains=q) |
                Q(grammatik_manosi__icontains=q)
            )
            
            # Search in WordSynonym
            synonym_q |= (
                Q(grammatical_word__icontains=q) |
                Q(translations__icontains=q) |
                Q(identity__icontains=q) |
                Q(synonyms__icontains=q)
            )
        
        # Search in GrammaticalForm with combined queries
        grammatical_forms = GrammaticalForm.objects.filter(form_q).distinct()

        # Search in UslubData with combined queries
        uslub_data = UslubData.objects.filter(uslub_q)

        # Search in WordSynonym with combined queries
        word_synonyms = WordSynonym.objects.filter(synonym_q)
        
        # Search in Sinonimlar model
        sinonimlar_q = Q()
        for q in queries:
            sinonimlar_q |= (
                Q(grammatik_manosi__icontains=q) |
                Q(sinonimlar__icontains=q) |
                Q(misol__icontains=q) |
                Q(english__icontains=q)
            )
        
        sinonimlar = Sinonimlar.objects.filter(sinonimlar_q)
        
        # Search in GrammatikManoData model
        grammatik_mano_q = Q()
        for q in queries:
            grammatik_mano_q |= (
                Q(grammatik_manosi__icontains=q) |
                Q(badiiy_uslub__icontains=q) |
                Q(ilmiy_uslub__icontains=q) |
                Q(publitsistik_uslub__icontains=q) |
                Q(rasmiy_uslub__icontains=q) |
                Q(sozlashuv_uslubi__icontains=q)
            )
        
        grammatik_mano = GrammatikManoData.objects.filter(grammatik_mano_q)
        
        # Combine all results into a list of dictionaries
        results = []
        
        for form in grammatical_forms:
            results.append({
                'type': 'grammatical_form',
                'title': form.term,
                'category': form.category.name,
                'description': form.grammatical_meaning,
                'translation': form.translation,
                'url': reverse('form_detail', kwargs={'pk': form.pk}),
            })

        for item in uslub_data:
            results.append({
                'type': 'uslub',
                'title': item.yordamchi_soz,
                'category': "Uslub ma'lumoti",
                'description': item.grammatik_manosi,
                'translation': item.maxsus_kodi,
                'url': reverse('uslub'),  # Link to the uslub page
            })

        for word in word_synonyms:
            results.append({
                'type': 'synonym',
                'title': word.grammatical_word,
                'category': 'Sinonimlar',
                'description': word.synonyms,
                'translation': word.translations,
                'url': reverse('word_synonyms'),  # Link to the synonyms page
            })
            
        for item in sinonimlar:
            results.append({
                'type': 'sinonimlar',
                'title': item.grammatik_manosi[:50] + ('...' if len(item.grammatik_manosi) > 50 else ''),
                'category': 'Sinonimlar',
                'description': item.sinonimlar,
                'translation': item.english,
                'url': reverse('sinonimlar'),  # Link to the sinonimlar page
            })
            
        for item in grammatik_mano:
            results.append({
                'type': 'grammatik_mano',
                'title': item.grammatik_manosi[:50] + ('...' if len(item.grammatik_manosi) > 50 else ''),
                'category': "Grammatik ma'no",
                'description': f"Badiiy: {item.badiiy_uslub[:30]}..." if item.badiiy_uslub else "",
                'translation': "",
                'url': reverse('grammatik_mano'),  # Link to the grammatik_mano page
            })

        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['total_count'] = len(self.get_queryset())
        return context 