"""budget URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from mybudget import views
from django.contrib.auth.views import logout
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^login/$','django.contrib.auth.views.login'),
    url(r'^new/$', views.post_new, name='post_new'),
    
    #url(r'^list/$', views.post_all_list, name='post_all_list'),
    url(r'^range_date/$', views.range_date, name='range_date'),
    url(r'^range_date3/$', views.range_date3, name='range_date3'),
    #url(r'^actual_list_short/$', views.post_actual_period_short, name='post_actual_period_short'),
    url(r'^end_period/$', views.end_period, name='end_period'),
    
    #url(r'^actual_list_short/(\d+)/(\d+)$', views.post_actual_period2, name='post_actual_period2'),
    #url(r'^your-name/$', views.test, name='test'),
    #url(r'^set_date/$', views.test, name='test'),

    url(r'^logout/$', logout, {'template_name': 'lista_wydatkow.html', 'next_page': '/login'}, name='log-out'),
    url(r'^period_list/$', views.period_list, name='period_list'),
    url(r'^history/(?P<wybrany_okres>\w+)/$', views.post_actual_period2, name='post_actual_period2'),
    url(r'^history/$', views.post_actual_period2, name='post_actual_period2'),
    url(r'^question/$', views.question, name='question'),
    url(r'^details/(?P<ids>\w+)/$', views.details, name='details'),
    url(r'^remove/(?P<ids>\w+)/$', views.remove, name='remove'),
    
    
]
