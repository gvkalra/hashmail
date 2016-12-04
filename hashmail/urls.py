"""hashmail URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

import hashapp.views

urlpatterns = [
    url(r'^$', hashapp.views.view_index),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='auth_logout'),
    url(r'^signup/', hashapp.views.register_user),
    url(r'^notifications/', hashapp.views.view_notifications),
    url(r'^publish/$', hashapp.views.publish_image),
    url(r'^publish/result', hashapp.views.publish_result, name='publish_result'),
    url(r'^subscribe', hashapp.views.manage_subscription),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
]