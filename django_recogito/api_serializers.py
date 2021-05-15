from rest_framework import serializers
from django_recogito.models import RecogitoAnnotation


class RecogitoAnnotationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RecogitoAnnotation
        fields = "__all__"
        depth = 1