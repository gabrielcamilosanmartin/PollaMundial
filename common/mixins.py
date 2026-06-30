from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Solo personal autorizado (is_staff) puede acceder."""

    def test_func(self):
        return self.request.user.is_staff
