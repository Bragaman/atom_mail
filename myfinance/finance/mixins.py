from django.contrib.auth.mixins import AccessMixin


class SuperUserRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_superuser):
            return self.handle_no_permission()
        return super(SuperUserRequiredMixin, self).dispatch(request, *args, **kwargs)