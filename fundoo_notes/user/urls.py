from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(),name="register"),
    path('login/', views.UserLoginView.as_view(),name="login"),
    path('verify/<str:token>/', views.verify_registered_user,name="verify"),
    # path('', views.index, name='home'),
    path('profile/', views.user_profile, name='profile'),
    path('loginpage/', views.user_login, name='login_page'),
    path('signupage/', views.user_signup, name='signup_page'),
    path('logoutpage/', views.user_logout, name='logout_page'),
]