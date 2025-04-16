from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from public_app.models import Client
from authentication.forms import LoginForm, SignUpTenantUser
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from authentication.models import TenantUser



class LoginIndexView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'index_login.html', {'login_form': login_form})
    
    def post(self, request):
        login_form = LoginForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('navigation')
        else:
            messages.error(request, 'Email/Nome de Usuário ou senha inválidos. Lembre-se de diferenciar letras maiúsculas de minúsculas.')
        return render(request, 'index_login.html', {'login_form': login_form})


class SignUpTenantUserView(View):
    def get(self, request, *args, **kwargs):
        print('template está sendo renderizado')
        signup_form = SignUpTenantUser()
        return render(request, 'signup_worker.html', {'signup_form': signup_form})

    def post(self, request):
        signup_form = SignUpTenantUser(data=request.POST)
        if signup_form.is_valid():
            signup_form.save()
            user = User.objects.filter(username=request.POST['username']).first()
            user.is_active = False
            user.save()
            TenantUser.objects.create(user=user, 
                                      cpf=request.POST['cpf'],                                                     function=request.POST['function'],
                                      created_by=request.user,
                                      tenant = request.tenant,
                                    )
            messages.success(request, 'Usuário criado com sucesso! Entre no e-mail para ativar sua conta.')
            return redirect('signup_tenant_user')
        return render(request, 'signup_worker.html', {'signup_form': signup_form})

    

class NavigationView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'navigation.html')
    

def logout_view(request):
    logout(request)
    messages.success(request, 'Usuário deslogado com sucesso!')
    return redirect('login_index')