from django.urls import path
from .views import (
    CategoryDetailView, FormDetailView, SearchResultsView,
    UslubView, YordamchiSozView, UmumiyBazaView, HomeView, WordSynonymView,
    GrammatikManoView, DavriylikiView, SinonimlarView,
    about, export_category, import_yordamchi_excel,
    import_sinonimlar_excel, import_grammatik_excel, import_davriylik_excel
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Home page
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('form/<int:pk>/', FormDetailView.as_view(), name='form_detail'),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('about/', about, name='about'),
    path('export/<int:category_id>/<str:format>/', export_category, name='export_category'),
    path('yordamchi-soz/', YordamchiSozView.as_view(), name='yordamchi_soz'),
    path('yordamchi-soz/umumiy-baza/', UmumiyBazaView.as_view(), name='umumiy_baza'),
    path('yordamchi-soz/import/', import_yordamchi_excel, name='import_yordamchi'),
    path('yordamchi-soz/sinonimlar/', SinonimlarView.as_view(), name='sinonimlar'),
    path('yordamchi-soz/import-sinonimlar/', import_sinonimlar_excel, name='import_sinonimlar'),
    path('yordamchi-soz/uslub/', UslubView.as_view(), name='uslub'),
    path('yordamchi-soz/word-synonyms/', WordSynonymView.as_view(), name='word_synonyms'),
    path('yordamchi-soz/grammatik-mano/', GrammatikManoView.as_view(), name='grammatik_mano'),
    path('yordamchi-soz/import-grammatik/', import_grammatik_excel, name='import_grammatik'),
    path('yordamchi-soz/davriylik/', DavriylikiView.as_view(), name='davriylik'),
    path('yordamchi-soz/import-davriylik/', import_davriylik_excel, name='import_davriylik'),
]