from django.urls import path 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
) 
from .views import UploadAvatarView,SignupView,MyProfileView,PublicProfileView, ChangePasswordView,UpdateProfileView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('my_profile/', MyProfileView.as_view(), name='my-profile'),
    path('update/profile',UpdateProfileView.as_view(), name='update-profile'),
    path('upload_avatar/', UploadAvatarView.as_view(), name='upload-avatar'),
    path('profiles/<uuid:user_id>/', PublicProfileView.as_view(), name='public-profile'),
    path('change_password', ChangePasswordView.as_view(), name='change-password')
]