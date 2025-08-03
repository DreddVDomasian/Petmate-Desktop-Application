from rest_framework import serializers
from .models import basicInfo, Pet, Service

class BasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = basicInfo
        fields = '__all__'

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    owner_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = '__all__'

    def get_owner_full_name(self, obj):
        return f"{obj.owner.firstName} {obj.owner.lastName}"