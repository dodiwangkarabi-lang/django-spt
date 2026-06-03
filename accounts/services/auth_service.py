from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from accounts.models import Profile
from django.db import transaction

ROLE_DASHBOARD_MAP = {
    'pegawai': 'core_pegawai_dashboard',
    'kasubag': 'core_kasubag_dashboard',
    'pimpinan': 'core_pimpinan_dashboard',
    
}

# def get_dashboard_url(user):
#     for group_name, url in ROLE_DASHBOARD_MAP.items():
#         if user.groups.filter(name=group_name).exists():
#             return url

#     return 'login'  # fallback

def login_user(request, username, password):
    user = authenticate(request, username=username, password=password)

    if not user:
        return None, "Username atau password salah"

    if not user.is_active:
        return None, "User tidak aktif"

    return user, None

def get_user_role(user):
    group = user.groups.first()
    return group.name if group else None


def get_dashboard_url(user):
    role = get_user_role(user)
    return ROLE_DASHBOARD_MAP.get(role, 'login')


class UserService:
    
    @staticmethod
    def update_user(user_id, data):
        user = get_object_or_404(User, id=user_id)
        
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        
        user.save()
        
        return user

    @staticmethod
    @transaction.atomic
    def update_profile(user_id, profile_data):
        user = get_object_or_404(User, id=user_id)
        
        # update user
        # for field in ["username", "email"]:
        #     if field in user_data:
        #         setattr(user, field, user_data[field])
        
        # user.save()
        
        # ambil atau buat
        profile_account, created = Profile.objects.get_or_create(user=user)
        
        # update profile
        for field in ["nama", "nip", "jabatan", "pangkat", "unit_kerja"]:
            if field in profile_data:
                setattr(profile_account, field, profile_data[field])
        
        profile_account.save()
        
        return user, profile_data

    @staticmethod
    def change_password(user_id, data):
        user = get_object_or_404(User, id=user_id)
        
        user.set_password(data.get('password'))
        user.save()
        
        return user

