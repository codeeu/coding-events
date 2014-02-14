from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'codeweekeu.', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'', include('web.urls')),
	url('', include('social.apps.django_app.urls', namespace='social')),

	#url(r'^login-error/$', 'django.views.generic.base.TemplateView', {'template': 'pages/login-error.html'}),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns(
	'',
	#url(r'^login/$', RedirectView, {'url': 'login/github'}),
    #url(r'^login/$', RedirectView, {'url': 'login/twitter'}),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
	    {'next_page': '/'}, name='logout'),
)
