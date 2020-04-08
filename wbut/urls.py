"""makautparser URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from wbut import views
from django.contrib.sitemaps.views import sitemap
from wbut.sitemap import StaticViewSitemap
from . import views
from django.views.generic import TemplateView



app_name = 'wbut'

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('', views.index, name="home"),
    path('colleges',views.collegeList,name="colleges"),
    path('view-result/<roll_no>/<semester>', views.viewResult, name="viewResult"),
    path('class-result/<roll_no>/<semester>', views.viewClassRank, name="viewClassResult"),
    path('result-page/', views.resultOverview, name="resultPage"),
    path('download-pdf/<roll_no>/<semester>', views.export, name="downloadPdf"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap'),
    path('contact-us', views.contactUs, name="contactUs"),
    path('privacy-policy', views.privacyPolicy, name="privacyPolicy"),
    path('about-us', views.aboutUs, name="aboutUs"),
    path('robots.txt', TemplateView.as_view(template_name="wbut/robots.txt", content_type='text/plain')),

]
