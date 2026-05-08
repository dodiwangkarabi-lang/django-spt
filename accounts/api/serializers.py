from django.contrib.auth.models import User, Group
from rest_framework import serializers
from accounts.models import Profile
from django.db import transaction

class UserSerializer(serializers.ModelSerializer):
    ROLE_CHOICES = [
        ("pegawai", "Pegawai"),
        ("pimpinan", "Pimpinan"),
        ("kasubag", "Kasubag"),
    ]
    
    role = serializers.ChoiceField(
        choices=ROLE_CHOICES,
        write_only=True
    )
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):

        role = validated_data.pop("role")

        user = User.objects.create_user(
            **validated_data
        )

        group = Group.objects.get(name=role)

        user.groups.add(group)

        return user
    
class ProfileSerializer(serializers.ModelSerializer):

    # username = serializers.CharField(write_only=True)

    password = serializers.CharField(write_only=True)
    
    ROLE_CHOICES = [
        ("pegawai", "Pegawai"),
        ("pimpinan", "Pimpinan"),
        ("kasubag", "Kasubag"),
    ]
    
    role = serializers.SlugRelatedField(
        queryset=Group.objects.all(),
        slug_field='name',
        write_only=True
    )
    
    role_display = serializers.SerializerMethodField()
    
    # role = serializers.ChoiceField(
    #     choices=ROLE_CHOICES,
    #     write_only=True
    # )

    class Meta:
        model = Profile
        fields = [
            "id",
            "nama",
            "nip",
            "password",
            "role",
            "role_display",
        ]
    
    def get_role_display(self, obj):
        group = obj.user.groups.first()
        return group.name if group else None
        
    
    
    def validate_nip(self, value):

        qs = User.objects.filter(username=value)

        # exclude user saat update
        if self.instance:
            qs = qs.exclude(id=self.instance.user.id)

        if qs.exists():
            raise serializers.ValidationError("NIP sudah digunakan.")

        return value

    @transaction.atomic
    def create(self, validated_data):

        # username = validated_data.pop("username")
        password = validated_data.pop("password")

        role = validated_data.pop("role")
        nip = validated_data.get("nip")

        user = User.objects.create_user(
            username=nip,
            password=password
        )

        group = Group.objects.get(name=role)

        user.groups.add(group)

        profile = Profile.objects.create(
            user=user,
            **validated_data
        )

        return profile