from django.contrib.auth.models import User

def get_user_by_role(role: str):
    """
    ambil user

    Args:
        role (str): role/peran user

    Returns:
        obj: instance object User
        
    Example:
        >>> user = UserService.get_user_by_role(role="pegawai")
    """
    return User.objects.filter(groups__name=role).first()

def get_pimpinan_user() -> User | None:
    return User.objects.filter(groups__name='pimpinan').first()

def get_kasubag_user() -> User | None:
    return User.objects.filter(groups__name='kasubag').first()

def get_pegawai_user(many=False) -> User | None:
    if many:
        return User.objects.filter(groups__name='pegawai')
    
    return User.objects.filter(groups__name='pegawai').first()
