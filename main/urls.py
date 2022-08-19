from django.urls import path

from .views import MainTemplateView, AboutTemplateView, AboutServicesTemplateView, ContactTemplateView, RobotsTxtView, \
    SitemapXmlView

urlpatterns = [
    path('', MainTemplateView.as_view(), name='main_page'),
    path('about_us/', AboutTemplateView.as_view(), name='about_page'),
    path('services/', AboutServicesTemplateView.as_view(), name='about_services_page'),
    path('contacts/', ContactTemplateView.as_view(), name='contact_page'),

    # robots.txt and sitemap.xml
    path('robots.txt', RobotsTxtView.as_view()),
    path('sitemap.xml', SitemapXmlView.as_view())
]
