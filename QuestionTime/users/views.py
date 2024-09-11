from django.shortcuts import render
from django_registration.backends.one_step.views import RegistrationView
from .forms import CustomUserForm



# Create your views here.
class MyRegistrationView(RegistrationView):
    form_class = CustomUserForm
    
    