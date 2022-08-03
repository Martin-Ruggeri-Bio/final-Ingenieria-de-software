from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from accounts.models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()

class UserProfileView(View):
    # el username llega como parametro con el get en la url
    def get(self, request, username,*args, **kwargs):
        user = get_object_or_404(User, username=username)
        profile = Profile.objects.get(user=user)
        #el contexto nos permite enviar informacion al template
        context={
            'user':user,
            'profile':profile
        }
        return render(request, 'users/detail.html', context)