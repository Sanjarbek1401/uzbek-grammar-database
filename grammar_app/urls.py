from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('form/<int:pk>/', views.FormDetailView.as_view(), name='form_detail'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('about/', views.about, name='about'),
]