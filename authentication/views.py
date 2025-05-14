from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from authentication.forms import LoginForm, SignUpTenantUser
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User
from authentication.models import TenantUser
from django.contrib.auth import authenticate
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse_lazy
from project.settings import DOMAIN_NAME



class LoginIndexView(View):

    def get(self, request):
        login_form = LoginForm()
        return render(request, 'index_login.html', {'login_form': login_form , 'DOMAIN_NAME': DOMAIN_NAME})

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

    
class SignUpTenantUserView(LoginRequiredMixin, View):
    permission_required = 'admin'

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
    
    
class ShowTenantUserView(LoginRequiredMixin, ListView):
    model = TenantUser
    template_name = 'show_worker.html'
    context_object_name = 'users'
    paginate_by = 10
    ordering = ['id']


class DeleteTenantUserView(LoginRequiredMixin, DeleteView):
    model = TenantUser
    template_name = 'delete_worker.html'
    success_url = reverse_lazy("show_tenant_users")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Usuário excluído com sucesso!")
        return super().delete(request, *args, **kwargs)


class UpdateTenantUserView(LoginRequiredMixin, UpdateView):
    model = TenantUser
    fields = ["function"]
    template_name = "update_worker.html"
    success_url = reverse_lazy("show_tenant_users")

    def form_valid(self, form):
        messages.success(self.request, "Função atualizada com sucesso!")
        return super().form_valid(form)


class ShowUserProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tenant_user = TenantUser.objects.filter(tenant=request.tenant, user=request.user).first()
        return render(request, 'show_profile.html', {'DOMAIN_NAME': DOMAIN_NAME, 'tenant_user': tenant_user})


class NavigationView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'navigation.html')
    

def logout_view(request):
    logout(request)
    messages.success(request, 'Usuário deslogado com sucesso!')
    return redirect('login_index')