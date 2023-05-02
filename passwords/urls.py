from django.urls import path
from .views import AddPasswordView, UpdatePasswordView, DeletePasswordView, PasswordListAPIView, ShowPasswordView

urlpatterns = [
    path('add/', AddPasswordView.as_view(), name='add_password'),
    path('<int:pk>/', ShowPasswordView.as_view(), name='password'),
    path('password_list/', PasswordListAPIView.as_view(), name='password_list'),
    path('<int:pk>/update/', UpdatePasswordView.as_view(), name='update_password'),
    path('<int:pk>/delete/', DeletePasswordView.as_view(), name='delete_password'),
]
