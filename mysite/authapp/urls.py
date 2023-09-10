from django.contrib.auth.views import LoginView
from django.urls import path

from .views import LogoutRedirect, get_cookies, set_cookies, \
    get_session, set_session, RegisterView, AboutMeView, UserUpdateView, UsersListView, UserDetailsView

app_name = 'authapp'

urlpatterns = [
    path('about-me/', AboutMeView.as_view(), name='about-me'),
    path('about-me/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('users-list/', UsersListView.as_view(), name='users-list'),
    path('users-details/<int:pk>/', UserDetailsView.as_view(), name='users-details'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='authapp/login.html',
                                     redirect_authenticated_user=True,), name='login'),
    path('logout/', LogoutRedirect.as_view(), name='logout'),
    path('set-cookies/', set_cookies, name='set-cookies'),
    path('get-cookies/', get_cookies, name='get-cookies'),
    path('set-session/', set_session, name='set-session'),
    path('get-session/', get_session, name='get-session'),

]
