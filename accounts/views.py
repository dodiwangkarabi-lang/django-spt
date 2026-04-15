from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
# from django.contrib import messages

# not allowed
from django.http import HttpResponseNotAllowed

from django.shortcuts import render, redirect
from .services.auth_service import get_dashboard_url, get_user_role, login_user

@login_required
def change_password(request):
    """catatan
    dalam request.POST = old_password, new_password, new_password2
    
    """
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            print("berhasil dirubah")
            user = form.save()
            update_session_auth_hash(request, user)  # supaya tidak logout
            
            return redirect("accounts_profile")
        else:
            print("gagal dirubah")
            print(form.errors)
            
            return render(request, 'pages/pegawai/edit-profile.html', {'form': form})
    # else:
    #     form = PasswordChangeForm(user=request.user)

    # return render(request, 'change_password.html', {'form': form})
    # return render(request, 'pages/pegawai/edit-profile.html', {'form': form})

    return redirect("accounts_profile")
    # return HttpResponseNotAllowed(['POST']) # hanya bisa diakses dengan method POST
     

def logout_view(request):
    logout(request)
    return redirect("accounts_login")

def register(request):
    template_name = "pages/guests/register.html"
    return render(request, template_name)

def login_view(request):
    template_name = "pages/guests/login.html"
    # kalau user sudah login → langsung lempar ke dashboard
    if request.user.is_authenticated:
        return redirect(get_dashboard_url(request.user))

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user, error = login_user(request, username, password)

        if error:
            return render(request, template_name, {
                "error": error
            })

        # proses login (session dibuat di sini)
        login(request, user)

        # redirect sesuai role (pakai service kamu)
        return redirect(get_dashboard_url(user))

    return render(request, template_name)