from rest_framework import serializers
from .models import *
from datetime import date

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
        source='owner',
        write_only=True
    )
    has_reminder = serializers.SerializerMethodField()
    age = serializers.ReadOnlyField()

    class Meta:
        model = Pet
        fields = '__all__'

    def validate(self, attrs):
        """
        Ensure stored_age is only saved if birthDay is not provided.
        """
        if attrs.get("birthDay"):
            # drop stored_age if birthday exists
            attrs["stored_age"] = None
        return attrs

    def get_has_reminder(self, obj):
        from django.utils.timezone import localdate
        today = localdate()

        has_appointment = WalkInAppointment.objects.filter(
            pet=obj,
            status__in=["pending", "overdue"]
        ).exists()

        has_service = Service.objects.filter(
            pet=obj,
            return_date__isnull=False,
            status__in=["pending", "overdue"]
        ).exists()

        return has_appointment or has_service




class ServiceSerializer(serializers.ModelSerializer):
    owner_full_name = serializers.SerializerMethodField()
    pet_name = serializers.SerializerMethodField()


    class Meta:
        model = Service
        fields = '__all__'

    def get_owner_full_name(self, obj):
        parts = [obj.owner.firstName, obj.owner.middleName, obj.owner.lastName]
        return " ".join(p for p in parts if p)  # skips None or ""

    def get_pet_name(self, obj):
        return obj.pet.petName




class WalkInSerializer(serializers.ModelSerializer):
    owner_full_name = serializers.SerializerMethodField()
    petName = serializers.SerializerMethodField()
    class Meta:
        model = WalkInAppointment
        fields = '__all__'
    def get_owner_full_name(self, obj):
        parts = [obj.owner.firstName, obj.owner.middleName, obj.owner.lastName]
        return " ".join(p for p in parts if p)  # skips None or ""

    def get_petName(self, obj):
        return obj.pet.petName
    




# FOR BOOKING ID
class WalkInAppointmentSerializer(serializers.ModelSerializer):
    booking_id = serializers.CharField(read_only=True)  # Make it read-only
    
    class Meta:
        model = WalkInAppointment
        fields = '__all__'