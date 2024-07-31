from django.shortcuts import redirect

# This mixins redirects already authenticated users from accessing the login page


class RedirectAuthUser(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('logistics:home')
        return super().dispatch(request, *args, **kwargs)
