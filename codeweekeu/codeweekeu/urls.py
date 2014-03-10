from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.conf import settings
from web.views.users import user_profile

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
	'',
	url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #Note: keep this urls last
    url(r'', include('web.urls')),
)

urlpatterns += patterns(
	'',
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
	    {'next_page': '/'}, name='logout'),
    url(r'^accounts/profile/$', user_profile, name='profile')
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('', (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
