from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'text-start'
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(
                Field('username',
                      placeholder='Usuário',
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
