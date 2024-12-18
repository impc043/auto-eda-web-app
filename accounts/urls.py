from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home" ),
    path('user_info/', views.user_info, name="user_info" ),
    path('login/', views.user_login, name="login" ),
    path('register/', views.user_register, name="register" ),
    path('logout/', views.user_logout, name="logout" ),
    path('update/', views.user_update, name="user_update" ),

    path('reset_password', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(), name="reset_password_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
   
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
For Forgot Password

1- submit email form                                             //PasswordResetView.as_view()
2- email sent success message                                    //PasswordResetDoneView.as_view()
3- link for password reset form provided in email                //PasswordResetConfirmView.as_view()
4- Password successfully changed message                         //PasswordResetCompleteView.as_view()
'''