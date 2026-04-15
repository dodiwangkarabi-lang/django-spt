from django.shortcuts import redirect
from functools import wraps
from .services.auth_service import get_user_role, get_dashboard_url

def role_required(role_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user_role = get_user_role(request.user)

            if user_role != role_name:
                return redirect(get_dashboard_url(request.user))

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# contoh penggunaan
# @role_required('pegawai')
# def dashboard_pegawai(request):
#     return render(request, "pegawai/dashboard.html")


# @role_required('kasubag')
# def dashboard_kasubag(request):
#     return render(request, "kasubag/dashboard.html")