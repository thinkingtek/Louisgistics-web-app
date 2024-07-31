from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetDoneView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import render, redirect
from .tokens import account_activation_token
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from datetime import timedelta, date
from django.contrib import messages
from .decorators import *
from .forms import *
from .mixins import *


User = get_user_model()


def deleteInactiveUsers(request):
    users = User.objects.filter(is_active=False)
    today = date.today()
    for user in users:
        start_date = user.date_joined.date()
        end_date = start_date + timedelta(days=3)

        if end_date < today:
            User.objects.get(pk=user.pk).delete()
    return render(request, 'account/delete_inactive_users.html')


@redirect_authenticated_user
def register(request):
    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email').lower()
            form.instance.email = email
            form.instance.first_name = form.cleaned_data.get(
                'first_name').title()
            form.instance.last_name = form.cleaned_data.get(
                'last_name').title()
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string('account/email_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            send_email = EmailMessage(subject, message, to=[email])
            send_email.send()
            return render(request, 'account/email_sent.html')
    else:
        form = UserRegForm()

    context = {
        'title': 'Sign-up',
        'form': form
    }
    return render(request, 'account/register.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        group = Group.objects.get(name='customer')
        user.groups.add(group)
        user.save()
        messages.success(
            request, f'{user.first_name} your account is successfully activated  you can now login')
        return redirect('login')
    else:
        return HttpResponse('registered succesfully and activation sent')
        # return render(request, 'account/activation_invalid.html')


@redirect_authenticated_user
def loginView(request):
    next = request.GET.get('next')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            login(request, user)
            if next:
                return redirect(next)
            return redirect('logistics:home')
    else:
        form = UserLoginForm()

    context = {'title': 'louisgistics | Login', 'form': form}
    return render(request, 'account/login.html', context)


@login_required
def dashboard(request):
    user = request.user
    email = request.user.email
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'email': email,
        'title': f'{user.first_name} | Dashboard',
        'u_form': u_form,
        'p_form': p_form,
        'dashboard_active': True,
    }
    return render(request, 'account/dashboard.html', context)


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    template_name = 'account/password_change.html'
    success_url = reverse_lazy('password-change-done')


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'account/password_change_done.html'
    success_url = reverse_lazy('password-change-done')


class ResetPassword(RedirectAuthUser, SuccessMessageMixin, PasswordResetView):
    template_name = 'account/password_reset.html'
    success_url = reverse_lazy('password-reset')
    success_message = 'An instruction has been sent to your email to reset your account password'


class ResetPasswordConfirm(RedirectAuthUser, PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('password-reset-complete')


class ResetPasswordComplete(RedirectAuthUser, PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class ResetDoneView(RedirectAuthUser, PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


# class UserLogoutView(LoginRequiredMixin, LogoutView):
#     def dispatch(self, request, *args, **kwargs):
#         messages.info(
#             request, f"{request.user.full_name} you have successfully logged out")
#         return super().dispatch(request, *args, **kwargs)


@redirect_unauthenticated_user
def userLogout(request):
    messages.info(
        request, f"{request.user.full_name} You have successfully logged out")
    logout(request)
    return redirect("login")
