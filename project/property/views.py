from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse(f"<h1>{request.tenant.company_name} Home Page</h1>")
