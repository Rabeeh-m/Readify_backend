from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from api import views


urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('', views.getRoutes),
    path('profile/', views.ProfileView.as_view(), name='get_profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='update_profile'),
]