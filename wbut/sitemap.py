from django.contrib import sitemaps
from django.urls import reverse
from wbut.views import resultOverview


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['wbut:home', 'wbut:colleges', 'wbut:contactUs']

    def location(self, item):
        return reverse(item)