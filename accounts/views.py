from accounts.forms import EditProfileForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from accounts.models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
from django.contrib import messages
from django.http import HttpResponse

User = get_user_model()


@login_required
def UserProfileView(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    followers = profile.followers.all()
    number_of_followers = len(followers)
    is_following = False
    if number_of_followers > 0:
        # si estoy en la lista de sus seguidores, yo soy seguidor
        for follower in followers:
            if follower == request.user:
                is_following = True
                break
    template = loader.get_template('users/detail.html')
    context = {
        'profile':profile,
        'number_of_followers':number_of_followers,
        'is_following': is_following,
    }
    return HttpResponse(template.render(context, request))


@login_required
def EditProfile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)
    user_basic_info = User.objects.get(id=user)
    if request.method == 'POST':
        form=EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user_basic_info.first_name = form.cleaned_data.get('first_name')
            user_basic_info.last_name = form.cleaned_data.get('last_name')
            profile.picture = form.cleaned_data.get('picture')
            profile.banner = form.cleaned_data.get('banner')
            profile.location = form.cleaned_data.get('location')
            profile.birthday = form.cleaned_data.get('birthday')
            profile.save()
            user_basic_info.save()
            return redirect('users:profile', username=request.user.username)
    else:
        form=EditProfileForm(instance=profile)
    context={
        'form':form,
    }
    return render(request, 'users/edit.html', context)

class AddFollower(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = Profile.objects.get(pk=pk)
		profile.followers.add(request.user)
		messages.add_message(
            self.request,
            messages.SUCCESS,
            'User Followed'
        )
		return redirect('users:profile', username=request.user.username)


class RemoveFollower(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = Profile.objects.get(pk=pk)
		profile.followers.remove(request.user)
		messages.add_message(
            self.request,
            messages.SUCCESS,
            'User Unfollowed'
        )
		return redirect('users:profile', username=request.user.username)


class ListFollowers(View):
    def get(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        followers = profile.followers.all()

        context = {
            'profile': profile,
            'followers': followers
        }

        return render(request, 'pages/social/followers_list.html', context)