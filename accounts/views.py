from django.contrib.auth import login
from django.shortcuts import render, redirect

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
