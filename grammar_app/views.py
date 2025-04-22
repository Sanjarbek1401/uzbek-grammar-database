# This file is deprecated - please use the views package instead
# It's kept for backward compatibility during the transition

# Import all views from their respective modules
from .views.base_views import home, about, HomeView
from .views.category_views import CategoryDetailView, FormDetailView, export_category
from .views.search_views import SearchResultsView
from .views.yordamchi_views import YordamchiSozView, UmumiyBazaView, import_yordamchi_excel
from .views.sinonimlar_views import SinonimlarView, import_sinonimlar_excel
from .views.uslub_views import UslubView
from .views.word_synonym_views import WordSynonymView
from .views.grammatik_mano_views import GrammatikManoView, import_grammatik_excel
from .views.davriylik_views import DavriylikiView, import_davriylik_excel

# Re-export all the views
__all__ = [
    'home', 'about', 'HomeView',
    'CategoryDetailView', 'FormDetailView', 'export_category',
    'SearchResultsView',
    'YordamchiSozView', 'UmumiyBazaView', 'import_yordamchi_excel',
    'SinonimlarView', 'import_sinonimlar_excel',
    'UslubView',
    'WordSynonymView',
    'GrammatikManoView', 'import_grammatik_excel',
    'DavriylikiView', 'import_davriylik_excel',
]