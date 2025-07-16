from django.urls import path 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
) 
from .views import GetUserPublicKeyView,UpdatePublicKeyView,GetUsersView,UploadAvatarView,SignupView,MyProfileView,PublicProfileView, ChangePasswordView,UpdateProfileView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('my_profile/', MyProfileView.as_view(), name='my-profile'),
    path('update/profile',UpdateProfileView.as_view(), name='update-profile'),
    path('upload_avatar/', UploadAvatarView.as_view(), name='upload-avatar'),
    path('save_public_key/', UpdatePublicKeyView.as_view(), name="save_public_key"),
    path('profiles/<uuid:user_id>/', PublicProfileView.as_view(), name='public-profile'),
    path('change_password', ChangePasswordView.as_view(), name='change-password'),
    path('users/', GetUsersView.as_view(),name='user-list'), # Getting all users for testing until we have a front end and no longer need everyone to have access to all users
    path('get_user_pk/<uuid:user_id>/', GetUserPublicKeyView.as_view(), name='get_public_key')
]