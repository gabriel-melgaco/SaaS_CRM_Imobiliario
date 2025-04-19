from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from authentication.forms import LoginForm, SignUpTenantUser
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from authentication.models import TenantUser
from django.contrib.auth import authenticate



class LoginIndexView(View):

    def get(self, request):
        login_form = LoginForm()
        return render(request, 'index_login.html', {'login_form': login_form})

    def post(self, request):
        login_form = LoginForm(data=request.POST)
        password = request.POST.get('password')

        if login_form.is_valid():
            user = User.objects.filter(username=login_form.cleaned_data['username']).first()
            
            if user is None:
                login_form.add_error(None, 'Usuário não encontrado.')
                return render(request, 'index_login.html', {'login_form': login_form})
            
            if not user.check_password(password):
                login_form.add_error(None, 'Senha incorreta.')
                return render(request, 'index_login.html', {'login_form': login_form})
            
            if not user.is_active:
                login_form.add_error(None, 'Acesse seu email para ativar sua conta.')
                return render(request, 'index_login.html', {'login_form': login_form})

            user_auth = authenticate(request, username=user.username, password=password)
            if user_auth is not None:
                login(request, user)
                return redirect('navigation')

        return render(request, 'index_login.html', {'login_form': login_form})

    
class SignUpTenantUserView(View):
    def get(self, request, *args, **kwargs):
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