from django.shortcuts import render


def store_index(request):
    return render(request, 'index.html')
