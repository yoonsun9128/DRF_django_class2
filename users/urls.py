from django.urls import path, include
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
app_name = 'user'

urlpatterns = [
    path('signup/', views.UserView.as_view(), name="UserView"),
    path('mock/', views.MockView.as_view(), name="mockview"),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name="follow"),
    path('<int:user_id>/', views.ProfileView.as_view(), name="profile"),
]
