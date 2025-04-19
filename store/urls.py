from .views import store_index
from django.urls import path  

urlpatterns = [
    path('', store_index, name='store_index'),
]
