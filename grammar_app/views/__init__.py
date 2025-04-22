# Import all views to maintain backward compatibility
from .core_views import home, HomeView, about, CategoryDetailView, FormDetailView
from .search_views import SearchResultsView
from .export_views import export_category
from .yordamchi_views import YordamchiSozView, UmumiyBazaView, import_yordamchi_excel
from .sinonimlar_views import SinonimlarView, import_sinonimlar_excel
from .uslub_views import UslubView
from .word_synonym_views import WordSynonymView
from .grammatik_mano_views import GrammatikManoView, import_grammatik_excel
from .davriylik_views import DavriylikiView, import_davriylik_excel

# Make all views available at the package level for backward compatibility
__all__ = [
    'home', 'HomeView', 'about', 'CategoryDetailView', 'FormDetailView',
    'SearchResultsView',
    'export_category',
    'YordamchiSozView', 'UmumiyBazaView', 'import_yordamchi_excel',
    'SinonimlarView', 'import_sinonimlar_excel',
    'UslubView',
    'WordSynonymView',
    'GrammatikManoView', 'import_grammatik_excel',
    'DavriylikiView', 'import_davriylik_excel',
] 