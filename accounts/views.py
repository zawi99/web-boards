from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from .forms import SingUpForm


def signup(request):
    if request.method == 'POST':
        form = SingUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SingUpForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/singup.html', context)


class UserAccountView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/account_detail.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name')
    template_name = 'accounts/account_update.html'
    success_url = reverse_lazy('account-detail')

    def get_object(self, queryset=None):
        return self.request.user
