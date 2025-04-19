from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit, HTML
from django.contrib.auth.models import User
from public_app.models import Client
from .models import TenantUser
from authentication.models import TenantUser
from django import forms
from django.db.models import Q
from django.db import connection
from public_app.models import Client
from django.contrib.auth.forms import UserCreationForm

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'text-start'
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(
                Field('username',
                      placeholder='Email ou nome de Usuário',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Field('password',
                      placeholder='Senha',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),  
            ),
            Div(
                Submit('submit', 'Entrar',
                       css_class='btn bg-gradient-dark w-100 my-4 mb-2'),
                css_class="text-center"
            )
        )

    def clean(self):
        username_or_email = self.cleaned_data.get('username')

        try:
            user = User.objects.get(Q(email=username_or_email) | Q(username=username_or_email))
        except User.DoesNotExist:
            raise forms.ValidationError('Este usuário/email não está cadastrado no nosso banco de dados. Solicite ao administrador do seu sistema.', code='invalid_login')
        
        self.cleaned_data['username'] = user

        current_schema = connection.schema_name
        tenant_user = TenantUser.objects.filter(user=user).first()
        client = Client.objects.filter(user=user).first()

     # Checks if the schema name is valid
        if tenant_user and tenant_user.tenant.schema_name == current_schema:
            return self.cleaned_data

    # checks if the schema name from user is valid
        if client and client.schema_name == current_schema:
            return self.cleaned_data

    # if any of the above conditions are not met, raise an error
        raise forms.ValidationError('Você não tem permissão para acessar este sistema.')


class SignUpTenantUser(UserCreationForm):
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)
    email = forms.EmailField(required=True)
    cpf = forms.CharField(required=True, max_length=11, min_length=11, label='CPF', widget=forms.TextInput(attrs={'placeholder': 'Digite seu CPF'}))
    function = forms.ChoiceField(choices=[('admin', 'Administrador'), ('recursos_humanos', 'Recursos Humanos'), ('corretor', 'Corretor de Imóveis')], label='Função')
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'cpf', 'function',]

    def __init__(self, *args, **kwargs):
        super(SignUpTenantUser, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'text-start'
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(
                Field('username',
                      placeholder='Nome de Usuário',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Field('first_name',
                      placeholder='Primeiro Nome',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Field('last_name',
                      placeholder='Último Nome',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Field('email',
                      placeholder='E-mail',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Field('password1',
                      placeholder='Digite a Senha',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Field('password2',
                      placeholder='Confirme a Senha',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Field('cpf',
                      placeholder='Digite o seu CPF',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),

            Div(
                HTML('<small class"form-text text-muted"> Escolha um função que seu colaborador irá desempenhar: </small>'),
                Field('function',
                      placeholder='Escolha uma função',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Submit('submit', 'Registrar',
                       css_class='btn btn-dark w-100 py-2 rounded-pill shadow'),
                css_class="text-center"
            ),
            
        )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'E-mail já cadastrado')
        return email
    
    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if Client.objects.filter(cpf=cpf).exists() or TenantUser.objects.filter(cpf=cpf).exists():
            self.add_error('cpf', 'CPF já cadastrado')
        return cpf
