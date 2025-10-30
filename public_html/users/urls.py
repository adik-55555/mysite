from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView,  PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy

app_name = "users"

urlpatterns = [
    #path('login/', views.login_user, name='login'), заменили на класс
    path('login/', views.LoginUser.as_view(), name='login'),
    #path('logout/', views.logout_user, name='logout'), заменили на класс
    path('logout/', LogoutView.as_view(), name='logout'),
    #path('password-reset/', 
         #PasswordResetView.as_view(template_name = "users/password_reset_form.html"),
         #name='password_reset'), заменили на нижнее с пространством имен users
     path('password-reset/',
         PasswordResetView.as_view(template_name="users/password_reset_form.html",
             email_template_name="users/password_reset_email.html",
             success_url=reverse_lazy("users:password_reset_done")
         ),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name = "users/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html", success_url=reverse_lazy("users:password_reset_complete")
         ), 
         name='password_reset_confirm'),
    path('password-reset/complete/', 
         PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name='password_reset_complete'),
    #path('register/', views.register, name='register'),  заменили на класс
    path('register/', views.RegisterUser.as_view(), name='register'),
]

