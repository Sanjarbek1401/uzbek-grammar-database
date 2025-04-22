# This file is kept for backward compatibility
# All views have been moved to the views/ package

from grammar_app.views.core_views import home, HomeView, about, CategoryDetailView, FormDetailView
from grammar_app.views.search_views import SearchResultsView
from grammar_app.views.export_views import export_category
from grammar_app.views.yordamchi_views import YordamchiSozView, UmumiyBazaView, import_yordamchi_excel
from grammar_app.views.sinonimlar_views import SinonimlarView, import_sinonimlar_excel
from grammar_app.views.uslub_views import UslubView
from grammar_app.views.word_synonym_views import WordSynonymView
from grammar_app.views.grammatik_mano_views import GrammatikManoView, import_grammatik_excel
from grammar_app.views.davriylik_views import DavriylikiView, import_davriylik_excel

# The views are now organized into the following modules:
# - core_views.py: Base views like home, HomeView, CategoryDetailView, FormDetailView, and about
# - search_views.py: SearchResultsView
# - export_views.py: export_category function
# - yordamchi_views.py: YordamchiSozView, UmumiyBazaView, and import_yordamchi_excel
# - sinonimlar_views.py: SinonimlarView and import_sinonimlar_excel
# - uslub_views.py: UslubView
# - word_synonym_views.py: WordSynonymView
# - grammatik_mano_views.py: GrammatikManoView and import_grammatik_excel
# - davriylik_views.py: DavriylikiView and import_davriylik_excel 