from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from store.models import UserProfile


def profile_require(function):
    def wrapper(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            profile = UserProfile.objects.filter(user=request.user)
            if not profile.exists():
                messages.error(request, '找不到用户资料，请重新登录')
                logout(request)
                return HttpResponseRedirect('/')

        return function(request, *args, **kwargs)

    return wrapper
 