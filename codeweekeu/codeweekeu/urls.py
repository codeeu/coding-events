from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'codeweekeu.', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'', include('web.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
