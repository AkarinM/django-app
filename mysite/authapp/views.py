from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DetailView

from authapp.models import Profile


class AboutMeView(TemplateView):
    template_name = 'authapp/about_me.html'


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('authapp:about-me')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)

        return response

class LogoutRedirect(LogoutView):
    next_page = reverse_lazy('authapp:login')


class UserUpdateView(UserPassesTestMixin, UpdateView):
    model = Profile
    fields = 'avatar',
    template_name = 'authapp/profile_update.html'

    def test_func(self):
        user = self.request.user
        return user.is_staff or self.get_object().user == user

    def get_success_url(self):
        return reverse('authapp:users-details', kwargs={'pk': self.object.pk})

    def get_object(self):
        user = User.objects.get(pk=self.kwargs.get('pk'))
        return user.profile

class UsersListView(ListView):
    template_name = 'authapp/users_list.html'
    queryset = User.objects.filter(is_active=True)
    context_object_name = 'users'


class UserDetailsView(DetailView):
    template_name = 'authapp/users_details.html'
    model = User
    context_object_name = 'userr'


def set_cookies(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookies set! ')
    response.set_cookie('name', 'Jhon', max_age=3600)
    return response


def get_cookies(request: HttpRequest) -> HttpResponse:
    cookies = request.COOKIES.get('name', 'Cookies is empty!')
    response = HttpResponse(f'{cookies}')
    return response


def set_session(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Session set! ')
    request.session['name'] = 'Jhon'
    return response


def get_session(request: HttpRequest) -> HttpResponse:
    session = request.session.get('name', 'Session is empty!')
    response = HttpResponse(f'{session}')
    return response

