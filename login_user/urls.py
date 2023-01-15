from django.urls import path, re_path

from .views import *
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path('', home, name='home'),
    path('profile/', ShowProfile.as_view(), name='profile'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/employee/', RegisterEmp.as_view(), name='register-emp'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('password/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('logout'), template_name='login_user/change_password.html'), name='change_password'),
]

