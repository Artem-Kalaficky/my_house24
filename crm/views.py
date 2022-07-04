from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from users.models import UserProfile


class StatisticsTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'crm/pages/statistics.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['new_users'] = UserProfile.objects.filter(status='new')
        context['count'] = len(context['new_users'])
        return self.render_to_response(context)
