from django.urls import path
from main import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'main'

urlpatterns = [
#	Main Page
    path('', views.MainView, name='main'),
#	LogIn
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
#	LogOut
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
#	SignUp/register
    path('signup/', views.RegView, name='signup'),
#	password change urls set
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html', success_url='/users/password_change_done'), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='password_reset_form.html', email_template_name='password_reset_email.html', subject_template_name='password_reset_subject.txt', success_url='/users/password_reset_done/', from_email='contact@deeptrading.info'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path("password_reset_confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', success_url='/users/password_reset_complete/'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),


]