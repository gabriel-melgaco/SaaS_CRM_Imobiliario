from django.forms import ModelForm
from django import forms
from public_app.models import Client, ActivationCode
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit, HTML
import re
from django_recaptcha.fields import ReCaptchaField
from django.db.models import Q #use for filtering the user by username OR email 
from django.shortcuts import redirect


class UserForm(UserCreationForm):
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
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


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'text-start'
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(
                Field('username',
                      placeholder='E-mail ou Nome de Usuário',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Div(
                    Field('password',
                          placeholder='Senha',
                          css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary',
                          autocomplete='current-password'
                    ),
                    HTML('<button type="button" class="btn btn-outline-secondary toggle-password" style="position:absolute; border: none; background: none; outline: none; cursor: pointer; right:10px; top:50%; transform:translateY(-50%);">👁</button>'),
                    css_class="position-relative"
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
            raise forms.ValidationError('Este usuário/email não está cadastrado no nosso banco de dados. Registre-se no nosso site pelo botão acima.', code='invalid_login')

        self.cleaned_data['username'] = user

        return self.cleaned_data



class ActivationForm(ModelForm):
    class Meta:
        model = ActivationCode
        fields = ['code']

    def __init__(self, *args, **kwargs):
        super(ActivationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'text-start'
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(
                Field('code',
                      placeholder='Código de Ativação',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Submit('submit', 'Ativar',
                       css_class='btn bg-gradient-dark w-100 my-4 mb-2'),
                css_class="text-center"
            )
        )

class PasswordResetForm(ModelForm): #screen to ask to reset the password
    captcha = ReCaptchaField(required=True)
    email = forms.EmailField(required=True)


    class Meta:
        model = User
        fields = ['email', 'captcha']

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'text-start'
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(
                Field('email',
                      placeholder='E-mail',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Field('captcha',), 
            ),
            Div(
                Submit('submit', 'Enviar',
                       css_class='btn bg-gradient-dark w-100 my-4 mb-2'),
                css_class="text-center"
            )
        )


class PasswordResetConfirmForm(forms.Form):  # Formulário para redefinição de senha
    password1 = forms.CharField(widget=forms.PasswordInput, label="Nova Senha")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirme a Nova Senha")

    def __init__(self, *args, **kwargs):
        super(PasswordResetConfirmForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'text-start'
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(
                Field('password1',
                      placeholder='Digite sua nova senha',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Field('password2',
                      placeholder='Digite novamente sua senha',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Submit('submit', 'Enviar',
                       css_class='btn bg-gradient-dark w-100 my-4 mb-2'
                ),
                css_class="text-center"
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem!")
        
        if password1:
            try:
                validate_password(password1)
            except ValidationError as e:
                self.add_error('password1', e)

        return cleaned_data




            
class ClientForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'text-start'
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(
                Field('company_name',
                      placeholder='Nome da Empresa',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Field('cpf',
                      placeholder='Digite seu CPF',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Field('dns_name',
                      placeholder='Escolha seu domínio: example.localhost',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Field('telephone',
                      placeholder='Digite seu Telefone',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Submit('submit', 'Adquirir Plano',
                       css_class='btn btn-dark w-100 py-2 rounded-pill shadow'),
                css_class="text-center"
            ),
        )
    
    class Meta:
        model = Client
        fields = ['company_name',
                  'cpf', 
                  'paid_until', 
                  'on_trial',
                  'dns_name',
                  'telephone',
                  ]
        
    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if not cpf.isdigit() or len(cpf) != 11:
            self.add_error('cpf', 'CPF deve conter apenas números e 11 dígitos')
        return cpf
    
        if Client.objects.filter(cpf=cpf).exists():
            self.add_error('cpf', 'CPF já cadastrado')
        return cpf

    def clean_dns_name(self):
        dns_name = self.cleaned_data['dns_name']
        
        if not dns_name:
            self.add_error('dns_name', 'O nome do DNS não pode estar vazio.')
            return dns_name
        
        if ' ' in dns_name:
            self.add_error('dns_name', 'O nome do DNS não pode conter espaços.')
            return dns_name
        
        if not re.match(r'^[a-zA-Z0-9-]+$', dns_name):
            self.add_error('dns_name', 'O nome do DNS só pode conter letras, números e hífens.')
            return dns_name
        
        if dns_name.startswith('-') or dns_name.endswith('-'):
            self.add_error('dns_name', 'O nome do DNS não pode começar ou terminar com hífen.')
            return dns_name
        
        if Client.objects.filter(dns_name=dns_name).exists():
            self.add_error('dns_name', 'Este nome de DNS já está em uso.')
            return dns_name
        
        return dns_name
    
    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        if not telephone.isdigit() or len(telephone) != 11:
            self.add_error('telephone', 'O telefone deve conter apenas números e 11 dígitos com DDD')
        return telephone