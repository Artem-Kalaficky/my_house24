from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from users.models import UserProfile


class SummaryTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'personal_cabinet/pages/summary.html'

