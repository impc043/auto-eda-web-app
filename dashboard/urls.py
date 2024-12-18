from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.dashboard, name="dashboard"),
    path('', views.dashboard, name="dashboard_new"),
    path('project/<str:pk>', views.user_project, name="user_project"),
    path('create_project', views.create_project, name="create_project"),
    path('delete_project/<str:pk>', views.delete_project, name="delete_project"),
     
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)