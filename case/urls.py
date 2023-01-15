from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('submit/', SubmitApplication.as_view(), name='submit_application'),
    path('', Expertise.as_view(), name='expertise'),
    path('<int:expertise_number>/', ExpertiseDetail.as_view(), name='expertise_detail'),
]