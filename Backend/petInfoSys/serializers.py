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
        from django.utils.timezone import localdate
        today = localdate()

        # 🔎 check walk-in appointments
        has_appt = WalkInAppointment.objects.filter(
            pet=obj,
            status="pending",
            date__lte=today
        ).exists()

        # 🔎 check services with return dates
        overdue_services = Service.objects.filter(
            pet=obj,
            return_date__isnull=False,
            return_date__lte=today
        )

        has_service = Service.objects.filter(
            pet=obj,
            return_date__isnull=False
        ).exists()
        return has_appt or has_service


class ServiceSerializer(serializers.ModelSerializer):
    owner_full_name = serializers.SerializerMethodField()
    pet_name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()  # <-- dynamic status

    class Meta:
        model = Service
        fields = '__all__'  # includes status + owner_full_name

    def get_owner_full_name(self, obj):
        return f"{obj.owner.firstName} {obj.owner.lastName}"

    def get_pet_name(self, obj):
        return obj.pet.petName

    def get_status(self, obj):
        if not obj.return_date:
            return None  # no status if no return date
        if obj.return_date < date.today():
            return "overdue"
        return "pending"



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