from rest_framework import viewsets

from recogito.api_serializers import RecogitoAnnotationSerializer
from recogito.models import RecogitoAnnotation


class RecogitoAnnotationViewSet(viewsets.ModelViewSet):
    queryset = RecogitoAnnotation.objects.all()
    serializer_class = RecogitoAnnotationSerializer
