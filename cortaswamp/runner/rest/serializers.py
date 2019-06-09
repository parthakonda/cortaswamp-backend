from runner.models import (
    Domain, JobHistory, InfraDetails, Measure
)
from rest_framework import serializers



class Domain(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'


class JobHistory(serializers.ModelSerializer):
    class Meta:
        model = JobHistory
        fields = '__all__'


class InfraDetails(serializers.ModelSerializer):
    class Meta:
        model = InfraDetails
        fields = '__all__'


class Measure(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = '__all__'
