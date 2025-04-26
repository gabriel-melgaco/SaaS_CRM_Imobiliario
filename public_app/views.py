from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from public_app.forms import UserForm, ClientForm, LoginForm, ActivationForm, PasswordResetForm, PasswordResetConfirmForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Client, ActivationCode, ResetPassword
from datetime import datetime, timedelta
from django.views import View
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from project.settings import DOMAIN_NAME
from django.db.models import Q #use for filtering the user by username OR email
from django.contrib.auth import authenticate



def index(request):
    if not request.user.is_authenticated:
        return render(request, 'landing_page.html')
    client = Client.objects.filter(user=request.user).first()

    return render(request, 'landing_page.html', {'client': client, 'DOMAIN_NAME': DOMAIN_NAME,})


class LoginView(View):

    def get(self, request):
        login_form = LoginForm()
        return render(request, 'login.html', {'login_form': login_form})

    def post(self, request):
        login_form = LoginForm(data=request.POST)
        password = request.POST.get('password')

        if login_form.is_valid():
            user = User.objects.filter(username=login_form.cleaned_data['username']).first()
            
            if user is None:
                login_form.add_error(None, 'Usuário não encontrado.')
                return render(request, 'login.html', {'login_form': login_form})

            if not user.check_password(password):
                login_form.add_error(None, 'Senha inválida. Por favor, tente novamente.')
                return render(request, 'login.html', {'login_form': login_form})

            if not user.is_active:
                return redirect('activation', user_id=user.id)

            user_auth = authenticate(request, username=user.username, password=password)
            if user_auth is not None:
                login(request, user)
                return redirect('home')

        return render(request, 'login.html', {'login_form': login_form})



class ActivationView(View):

    def get(self, request, user_id):
        activation_form = ActivationForm()
        return render(request, 'activation.html', {'activation_form': activation_form, 'user_id': user_id})
    
    def post(self, request, user_id):
        activation_form = ActivationForm(data=request.POST)
        
        if activation_form.is_valid():
            code = activation_form.cleaned_data['code']
            try:
                activation_code = ActivationCode.objects.get(user_id=user_id, code=code)
                user = activation_code.user 
                user.is_active = True
                user.save()
                
                activation_code.delete()

                messages.success(request, 'Usuário ativado com sucesso!')
                return redirect('login')
            
            except ActivationCode.DoesNotExist:
                return render(request, 'activation.html', {
                    'activation_form': activation_form,
                    'error': 'Código de ativação inválido ou expirado.',
                    'user_id': user_id,
                })
        
        return render(request, 'activation.html', {'activation_form': activation_form, 'user_id': user_id})


class RegisterView(View):
    
    def get(self, request):
        user_form = UserForm()
        return render(request, 'register.html', {'user_form': user_form})
    
    def post(self, request):
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user_form.save()
            user = User.objects.filter(username=request.POST['username']).first()
            user.is_active = False
            user.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('login')
        
        return render(request, 'register.html', {'user_form': user_form})


class PasswordResetView(View): # Open a page to insert the e-mail and ask for a password change
    
    def get(self, request):
        password_form = PasswordResetForm()
        return render(request, 'reset_password.html', {'password_form': password_form})

    def post(self, request):
        password_form = PasswordResetForm(data=request.POST)

        if password_form.is_valid():
            email = password_form.cleaned_data.get('email')  
            user = User.objects.filter(email=email).first()

            if user:
                print('##### USUÁRIO ENCONTRADO #####')
                print(user.email)
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(user)
                ResetPassword.objects.create(user=user, token=token)

                messages.info(request, 'Se o seu e-mail estiver cadastrado em nossa base de dados, você receberá um e-mail com instruções para redefinir sua senha.')
                return redirect('login')
        else:
            return render(request, 'reset_password.html', {
                'password_form': password_form,
                'message': 'Erro ao processar o formulário. Clique em não sou um robô para prosseguir!'
            })

        print('##### USUÁRIO NÃO ENCONTRADO #####')
        messages.info(request, 'Se o seu e-mail estiver cadastrado em nossa base de dados, você receberá um e-mail com instruções para redefinir sua senha.')
        return redirect('login')


class PasswordResetConfirmView(View): #Open the reset password page with a token

    def get(self, request, token):
        reset_token = ResetPassword.objects.filter(token=token).first()
        
        if not reset_token:
            return render(request, 'reset_password_confirm.html', {
                'error': 'Link inválido ou expirado.'
            })
        
        #Check if the token has more than 15 minuts
        if reset_token.created_at <= timezone.now() - timezone.timedelta(minutes=15): 
            reset_token.delete() 
            return render(request, 'reset_password_confirm.html', {
                'error': 'Link expirado. Solicite um novo link de redefinição de senha.'
            })

        password_reset_confirm_form = PasswordResetConfirmForm()
        return render(request, 'reset_password_confirm.html', {
            'password_reset_confirm_form': password_reset_confirm_form,
            'token': token,
        })
    
    def post(self, request, token):
        password_reset_confirm_form = PasswordResetConfirmForm(data=request.POST)
        reset_token = ResetPassword.objects.filter(token=token).first()

        if password_reset_confirm_form.is_valid():
            user = reset_token.user
            new_password = password_reset_confirm_form.cleaned_data['password1']
            user.set_password(new_password)
            user.save()
            reset_token.delete()
            print("Token excluído com sucesso!")

            messages.success(request, 'Sua senha foi redefinida com sucesso!')
            return redirect('login')

        else:
            return render(request, 'reset_password_confirm.html', {
                'password_reset_confirm_form': password_reset_confirm_form,
                'token': token,
            })


class RegisterClientView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = "redirect_to"
    
    def get(self, request):
        client_form = ClientForm()
        client = Client.objects.filter(user=request.user).first()
        return render(request, 'register_client.html', {'client_form': client_form, 'client': client})

    def post(self, request):
        user = request.user
        client = Client.objects.filter(user=user).first()
        client_form = ClientForm(request.POST)
        if client_form.is_valid() and not client:
            client = client_form.save(commit=False)
            client.paid_until = datetime.now() + timedelta(days=365)
            client.schema_name = client.dns_name
            client.user = user
            client.save()

            admin_group, _ = Group.objects.get_or_create(name='admin')
            user.groups.add(admin_group)

            
            print(f"Novo client criado: {client.company_name} para {client.user.username}")

            tenant_url = f"http://{client.dns_name}.{DOMAIN_NAME}"

            return HttpResponseRedirect(tenant_url)
        return render(request, 'register_client.html', {'client_form': client_form, 'client': client})


def logout_view(request):
    logout(request)
    return redirect('home')