import secrets
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView
from users.forms import UserRegisterForm, UserPasswordResetForm, ManagerUpdateView, UserProfileForm
from users.models import User
from config.settings import DEFAULT_FROM_EMAIL


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.set_password(user.password)
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение адреса элетронной почты',
            message=f'Доброго времени, для подтверждения перейдите по ссылке  {url}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserPasswordResetView(PasswordResetView, BaseUserManager):
    model = User
    form_class = UserPasswordResetForm
    template_name = 'users/password_reset_form.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form, make_random_password=None):
        if self.request.method == 'POST':
            user_email = self.request.POST.get('email')
            user = User.objects.filter(email=user_email).first()
            if user:
                new_password = BaseUserManager().make_random_password()
                user.set_password(new_password)
                user.save()
                try:
                    send_mail(
                            subject="Восстановление пароля",
                            message=f"Доброго времени! Ваш новый пароль:  {new_password}",
                            from_email=DEFAULT_FROM_EMAIL,
                            recipient_list=[user.email]
                            )
                except Exception:
                    print(f'Ошибка при отправке на почту {user_email}')
                return HttpResponseRedirect(reverse('users:login'))

        return super().form_valid(form)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    login_url = "/users/login/"

    def get_queryset(self):
        return User.objects.filter(is_superuser=False).exclude(groups__name='manager')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class ManagerUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ManagerUpdateView
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:users')
    login_url = "/users/login/"
