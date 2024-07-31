from django.shortcuts import redirect


class StaffUserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.groups.filter(name="staff").exists():
            return redirect("logistics:home")
        return super().dispatch(request, *args, **kwargs)
