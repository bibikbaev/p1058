from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('main/<int:ch_number>/', ChecklistDetailMain.as_view(), name='checklist_main'),
    path('<int:ch_number>/', ChecklistDetail.as_view(), name='checklist_detail'),
]

handler500 = 'checklist.views.handler500'