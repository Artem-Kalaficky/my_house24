from django.shortcuts import render
from django.views.generic import TemplateView


class StatisticsTemplateView(TemplateView):
    template_name = 'crm/pages/statistics.html'
