from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import HttpResponse
from public_app.models import Client
from authentication.forms import LoginForm

def login_index(request):
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request, data=request.POST) 
        if login_form.is_valid():
            user = login_form.get_user()
            client = Client.objects.get(schema_name=request.tenant.schema_name)
            if user == client.user:
                login(request, user)
                return HttpResponse(f"<h1>Bem vindo {user.username}</h1>")
            else:
                login_form.add_error(None, "Usuário não pertencente a este cliente.")
        else:
            login_form.add_error(None, "Usuário ou senha inválidos.") 
    
    return render(request, 'index_login.html', {'login_form': login_form})


def logout_view(request):
    logout(request)
    return redirect('login_index')