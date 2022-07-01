from django.shortcuts import render
from django.views.generic import TemplateView


class SummaryTemplateView(TemplateView):
    template_name = 'personal_cabinet/pages/summary.html'
