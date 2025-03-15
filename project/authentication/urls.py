from authentication.views import login_index, logout_view
from django.urls import path

urlpatterns = [
    path('login/', login_index, name='login_index'),
    path('logout/', logout_view, name='logout_view'),
]