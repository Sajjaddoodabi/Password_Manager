from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterView, UserView, ChangePasswordView, UpdateUserView, ResetPasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserView.as_view(), name='user_view'),
    path('me/change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('me/update/', UpdateUserView.as_view(), name='update_user'),
    path('me/reset/', ResetPasswordView.as_view(), name='update_user'),
]
