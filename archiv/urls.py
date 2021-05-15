from django.urls import path

from . import views

urlpatterns = [
    path('works/<int:pk>/', views.WorkDetailView.as_view(), name='work_detail'),
    path('manifestations/<int:pk>/', views.ManifestationDetailView.as_view(), name='manifestation_detail'),
    path('works/manifestimport/<int:pk>/', views.import_manifestations, name='import_manifestations'),
    path('collations/<int:pk>/', views.CollationDetailView.as_view(), name='collation_detail'),
    path('collations/create/', views.CollationCreateView.as_view(), name='collation_create'),
    path('collations/collate/<int:pk>', views.collate_collation, name='collate_collation'),
    path('', views.HomePageView.as_view(), name='index'),
    path('imprint', views.ImprintView.as_view(), name='imprint'),
]