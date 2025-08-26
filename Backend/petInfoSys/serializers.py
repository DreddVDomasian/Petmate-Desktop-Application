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
        source='owner',  # maps to the FK
        write_only=True
    )
    has_reminder = serializers.SerializerMethodField()
    class Meta:
        model = Pet
        fields = '__all__'

    def get_has_reminder(self, obj):
        # ✅ Avoid circular imports
        from django.utils.timezone import localdate
        today = localdate()

        # 🔎 Appointments that still need action (pending or overdue only)
        has_appointment = WalkInAppointment.objects.filter(
            pet=obj,
            status__in=["pending", "overdue"]
        ).exists()

        # 🔎 Services that still need action (pending or overdue only)
        has_service = Service.objects.filter(
            pet=obj,
            return_date__isnull=False,
            status__in=["pending", "overdue"]
        ).exists()

        # ✅ Only true if something is still pending/overdue
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