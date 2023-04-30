from django.urls import path
from .views import AddPasswordView

urlpatterns = [
    path('add/', AddPasswordView.as_view(), name='add_password'),
]
