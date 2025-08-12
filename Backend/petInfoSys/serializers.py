from rest_framework import serializers
from .models import *

class BasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = basicInfo
        fields = '__all__'

class PetSerializer(serializers.ModelSerializer):
    # For reading
    owner = BasicInfoSerializer(read_only=True)
    # For writing
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=basicInfo.objects.all(),
        source='owner',  # maps to the FK
        write_only=True
    )

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



class WalkInSerializer(serializers.ModelSerializer):
    owner_full_name = serializers.SerializerMethodField()
    petName = serializers.SerializerMethodField()
    class Meta:
        model = WalkInAppointment
        fields = '__all__'
    def get_owner_full_name(self, obj):
        return f"{obj.owner.firstName} {obj.owner.lastName}"

    def get_petName(self, obj):
        return obj.pet.petName