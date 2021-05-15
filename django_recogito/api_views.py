from rest_framework import viewsets

from django_recogito.api_serializers import RecogitoAnnotationSerializer
from django_recogito.models import RecogitoAnnotation


class RecogitoAnnotationViewSet(viewsets.ModelViewSet):
    queryset = RecogitoAnnotation.objects.all()
    serializer_class = RecogitoAnnotationSerializer
