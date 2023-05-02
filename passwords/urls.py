from django.urls import path
from .views import AddPasswordView, UpdatePasswordView

urlpatterns = [
    path('add/', AddPasswordView.as_view(), name='add_password'),
    path('<int:id>/update/', UpdatePasswordView.as_view(), name='update_password'),
]
