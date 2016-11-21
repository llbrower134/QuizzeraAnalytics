from django.conf.urls import include, url
from django.contrib import admin
import django_cas_ng.views

urlpatterns = [
    url(r'^', include('dashboard.urls', namespace='dashboard')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', django_cas_ng.views.login, name='cas_ng_login'),
    url(r'^accounts/logout/$', django_cas_ng.views.logout, name='cas_ng_logout'),
]
