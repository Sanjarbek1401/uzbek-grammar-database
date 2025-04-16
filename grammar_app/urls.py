from django.urls import path
from . import views
from .views import UslubView, YordamchiSozView, HomeView, WordSynonymView, CodedWordView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Home page
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('form/<int:pk>/', views.FormDetailView.as_view(), name='form_detail'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('about/', views.about, name='about'),
    path('export/<int:category_id>/<str:format>/', views.export_category, name='export_category'),
    path('yordamchi-soz/', YordamchiSozView.as_view(), name='yordamchi_soz'),
    path('yordamchi-soz/umumiy-baza/', views.UmumiyBazaView.as_view(), name='umumiy_baza'),
    path('yordamchi-soz/import/', views.import_yordamchi_excel, name='import_yordamchi'),
    path('yordamchi-soz/sinonimlar/', views.SinonimlarView.as_view(), name='sinonimlar'),
    path('yordamchi-soz/uslub/', UslubView.as_view(), name='uslub'),
    path('yordamchi-soz/word-synonyms/', WordSynonymView.as_view(), name='word_synonyms'),
    path('yordamchi-soz/coded-words/', CodedWordView.as_view(), name='coded_words'),
]