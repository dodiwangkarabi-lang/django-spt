from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps

# contoh penggunaan
# @roles_required('admin', 'dosen')
# def halaman_dosen(request):

def roles_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Harus login")
            
            # Ambil semua nama group user
            user_groups = request.user.groups.values_list('name', flat=True)

            # if request.user.role not in roles:
            if not any(group in user_groups for group in roles):
                return HttpResponseForbidden("Akses ditolak")

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# def role_required(role):
#     def decorator(view_func):
#         def _wrapped_view(request, *args, **kwargs):
#             if not request.user.is_authenticated:
#                 return HttpResponseForbidden("Harus login")

#             if request.user.role != role:
#                 return HttpResponseForbidden("Akses ditolak")

#             return view_func(request, *args, **kwargs)
#         return _wrapped_view
#     return decorator

# def roles_required(*roles):
#     def decorator(view_func):
#         def _wrapped_view(request, *args, **kwargs):
#             if not request.user.is_authenticated:
#                 return HttpResponseForbidden("Harus login")

#             if request.user.role not in roles:
#                 return HttpResponseForbidden("Akses ditolak")

#             return view_func(request, *args, **kwargs)
#         return _wrapped_view
#     return decorator

# def roles_required(*roles):
#     def decorator(view_func):
#         def _wrapped_view(request, *args, **kwargs):
#             if not request.user.is_authenticated:
#                 return redirect('login')

#             if request.user.role not in roles:
#                 return redirect('unauthorized')

#             return view_func(request, *args, **kwargs)
#         return _wrapped_view
#     return decorator