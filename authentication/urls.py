from authentication.views import LoginIndexView, logout_view, NavigationView, SignUpTenantUserView
from django.urls import path

urlpatterns = [
    path('login/', LoginIndexView.as_view(), name='login_index'),
    path('logout/', logout_view, name='logout_view'),
    path('navigation/', NavigationView.as_view(), name='navigation'),
    path('signup/', SignUpTenantUserView.as_view(), name='signup_tenant_user'),
]