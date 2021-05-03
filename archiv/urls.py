from django.urls import path

from . import views

urlpatterns = [
    path('works/<int:pk>/', views.WorkDetailView.as_view(), name='work_detail'),
    path('', views.HomePageView.as_view(), name='index'),
    path('imprint', views.ImprintView.as_view(), name='imprint'),
]