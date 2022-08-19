from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from .models import MainPage, ContactPage, Block, AboutPage, Photo, Document, AboutService, ServicePage


class MainTemplateView(TemplateView):
    template_name = 'main/pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_page'] = get_object_or_404(MainPage, pk=1)
        context['contact'] = get_object_or_404(ContactPage, pk=1)
        context['blocks'] = Block.objects.all()
        return context


class AboutTemplateView(TemplateView):
    template_name = 'main/pages/about_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about_page'] = get_object_or_404(AboutPage, pk=1)
        context['gallery'] = Photo.objects.all()
        context['documents'] = Document.objects.all()
        return context


class AboutServicesTemplateView(TemplateView):
    template_name = 'main/pages/about_services_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = get_object_or_404(ServicePage, pk=1)
        context['services'] = AboutService.objects.all()
        return context


class ContactTemplateView(TemplateView):
    template_name = 'main/pages/contact_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = get_object_or_404(ContactPage, pk=1)
        return context


# region robots.txt and sitemap.xml
class RobotsTxtView(TemplateView):
    template_name = 'elements/robots.txt'
    content_type = 'text/plain'


class SitemapXmlView(TemplateView):
    template_name = 'elements/sitemap.xml'
    content_type = 'application/xml'
# endregion robots.txt and sitemap.xml
