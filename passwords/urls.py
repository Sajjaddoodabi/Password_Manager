from django.urls import path
from .views import AddPasswordView, UpdatePasswordView, DeletePasswordView, PasswordListAPIView

urlpatterns = [
    path('add/', AddPasswordView.as_view(), name='add_password'),
    path('password_list/', PasswordListAPIView.as_view(), name='password_list'),
    path('<int:id>/update/', UpdatePasswordView.as_view(), name='update_password'),
    path('<int:id>/delete/', DeletePasswordView.as_view(), name='delete_password'),
]
