from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from recogito import api_views
router = routers.DefaultRouter()
router.register(r'recogitoannotations', api_views.RecogitoAnnotationViewSet)


urlpatterns = [
    path(r'api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('', include('archiv.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
