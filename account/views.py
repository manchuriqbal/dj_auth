from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout
from django.views import generic
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from .forms import LoginForms, RegistationForms
from .mixins import LogoutRequiredMixin


@method_decorator(never_cache, name="dispatch")
class Home(LoginRequiredMixin, generic.TemplateView):
    login_url = 'login'
    template_name = "account/home.html"

@method_decorator(never_cache, name="dispatch")
class Login(LogoutRequiredMixin ,generic.View):
    def get(self, *args, **kwargs):
        form = LoginForms()
        context = { 'form' : form }
        return render(self.request, "account/login.html", context)

    def post(self, *args, **kwargs):
        form = LoginForms(self.request.POST)

        if form.is_valid():
            user = authenticate(
                self.request,
                username = form.cleaned_data.get('username'),
                password = form.cleaned_data.get('password')
            )
            if user:
                login(self.request, user)
                return redirect('home')
            
            else:
                messages.warning(self.request, 'Worng credentials')
                return redirect('login')

        return render(self.request, "account/login.html", {'form':form})

class Logout(generic.View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('login')
    

@method_decorator(never_cache, name="dispatch")
class Registation(LogoutRequiredMixin, generic.CreateView):
    template_name = 'account/registation.html'
    success_url = reverse_lazy('login')
    form_class = RegistationForms

    def form_valid(self, form):
        messages.success(self.request, 'Registation Successfull!')
        return super().form_valid(form)
    
    
    
