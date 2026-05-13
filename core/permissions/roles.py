ROLE_PIMPINAN = "pimpinan"
ROLE_KASUBAG = "kasubag"
ROLE_PEGAWAI = "pegawai"

def has_role(user, role_name):
    return user.groups.filter(name=role_name).exists()

def is_pimpinan(user):
    return has_role(user, ROLE_PIMPINAN)

def is_pegawai(user):
    return has_role(user, ROLE_PEGAWAI)

def is_kasubag(user):
    return has_role(user, ROLE_KASUBAG)