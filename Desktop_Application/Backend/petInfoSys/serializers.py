from rest_framework import serializers
from .models import *
from datetime import date

class DesktopUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesktopUser
        fields = '__all__'

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
        write_only=True,
        required=False
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
            status__in=["pending", "overdue"],
            request="accepted"
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
    service_type = serializers.CharField(source='service_type.name', read_only=True)
    service_type_name = serializers.CharField(source='service_type.name', read_only=True)
    service_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceType.objects.all(),
        source='service_type',
        write_only=True,
        required=True
    )

    class Meta:
        model = Service
        fields = [
            'id', 'owner', 'pet', 'service_type', 'service_type_id',
            'service_type_name', 'date', 'return_date', 'date_added',
            'notes', 'status', 'owner_full_name', 'pet_name'
        ]

    def get_owner_full_name(self, obj):
        parts = [obj.owner.firstName, obj.owner.middleName, obj.owner.lastName]
        return " ".join(p for p in parts if p)

    def get_pet_name(self, obj):
        return obj.pet.petName


class WalkInSerializer(serializers.ModelSerializer):
    owner_full_name = serializers.SerializerMethodField()
    petName = serializers.SerializerMethodField()
    service_type_name = serializers.CharField(source='service_type.name', read_only=True)
    service_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceType.objects.all(),
        source='service_type',
        write_only=True,
        required=True
    )

    owner = BasicInfoSerializer(read_only=True)
    pet = PetSerializer(read_only=True)

    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=basicInfo.objects.all(),
        source='owner',
        write_only=True,
        required=False
    )
    pet_id = serializers.PrimaryKeyRelatedField(
        queryset=Pet.objects.all(),
        source='pet',
        write_only=True
    )

    class Meta:
        model = WalkInAppointment
        fields = [
            'id', 'booking_id', 'owner', 'pet', 'owner_id', 'pet_id',
            'date', 'prefTime', 'status', 'service_type', 'service_type_id',
            'service_type_name', 'request', 'created_at',
            'owner_full_name', 'petName'
        ]

    def get_owner_full_name(self, obj):
        parts = [obj.owner.firstName, obj.owner.middleName, obj.owner.lastName]
        return " ".join(p for p in parts if p)

    def get_petName(self, obj):
        return obj.pet.petName

    def create(self, validated_data):
        # Auto-set owner from pet if not provided (for web appointments)
        if 'owner' not in validated_data and 'pet' in validated_data:
            validated_data['owner'] = validated_data['pet'].owner

        return super().create(validated_data)


class OfficeHoursSerializer(serializers.ModelSerializer):
    start_time = serializers.TimeField(format='%H:%M:%S', required=False, allow_null=True)
    end_time = serializers.TimeField(format='%H:%M:%S', required=False, allow_null=True)

    class Meta:
        model = OfficeHours
        fields = ['id', 'day', 'status', 'start_time', 'end_time']


class ServiceTypeSerializer(serializers.ModelSerializer):
    can_delete = serializers.SerializerMethodField()

    class Meta:
        model = ServiceType
        fields = ['id', 'name', 'description', 'is_default', 'is_active', 'can_delete', 'created_at', 'updated_at']
        read_only_fields = ['is_default', 'created_at', 'updated_at']

    def get_can_delete(self, obj):
        # You can add logic here if needed
        return True

    def validate_name(self, value):
        # Check for duplicate names (case-insensitive)
        if ServiceType.objects.filter(name__iexact=value).exists():
            if self.instance and self.instance.name.lower() == value.lower():
                return value
            raise serializers.ValidationError("A service type with this name already exists.")
        return value.strip().title()


# -----------------WALKIN TO NEW ACCOUNT SYNC---------------------

class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerification
        fields = ['email', 'otp', 'patient_id']
        read_only_fields = ['otp', 'created_at', 'expires_at', 'verified', 'user_account_created']


class ClaimAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        # Password strength validation
        password = data['password']
        if len(password) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long."})
        if not any(char.isupper() for char in password):
            raise serializers.ValidationError({"password": "Password must contain at least one uppercase letter."})
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError({"password": "Password must contain at least one number."})

        return data