from authentication.views import LoginIndexView, logout_view, NavigationView, SignUpTenantUserView, ShowTenantUserView, DeleteTenantUserView, UpdateTenantUserView, ShowUserProfileView
from django.views.generic import TemplateView
from django.urls import path

urlpatterns = [
    path('login/', LoginIndexView.as_view(), name='login_index'),
    path('logout/', logout_view, name='logout_view'),
    path('navigation/', NavigationView.as_view(), name='navigation'),
    path('signup/', SignUpTenantUserView.as_view(), name='signup_tenant_user'),
    path('show_tenantusers/', ShowTenantUserView.as_view(), name='show_tenant_users'),
    path('delete_tenantuser/<int:pk>/', DeleteTenantUserView.as_view(), name='delete_tenant_user'),
    path('update_tenantuser/<int:pk>/', UpdateTenantUserView.as_view(), name='update_tenant_user'),
    path('show_profile/', ShowUserProfileView.as_view(), name='show_profile'),
    path('permission_denied/', TemplateView.as_view(template_name="permission_denied.html"), name='permission_denied'),
]