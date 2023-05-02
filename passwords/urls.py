from django.urls import path
from .views import AddPasswordView, UpdatePasswordView, DeletePasswordView

urlpatterns = [
    path('add/', AddPasswordView.as_view(), name='add_password'),
    path('<int:id>/update/', UpdatePasswordView.as_view(), name='update_password'),
    path('<int:id>/delete/', DeletePasswordView.as_view(), name='delete_password'),
]
