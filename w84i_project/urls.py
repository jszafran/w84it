""" Default urlconf for w84i_project """

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import index, sitemap
from django.views.generic.base import TemplateView
from django.views.defaults import (permission_denied,
                                   page_not_found,
                                   server_error)
from users import views as user_views
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns


sitemaps = {
    # Fill me with sitemaps
}

urlpatterns = i18n_patterns(
    # url(r'', include('base.urls')),

    # Admin
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Sitemap
    url(r'^sitemap\.xml$', index, {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', sitemap, {'sitemaps': sitemaps}),

    # robots.txt
    url(r'^robots\.txt$',
        TemplateView.as_view(
            template_name='robots.txt',
            content_type='text/plain')
        ),

    # Users Registration
    # url(r'^register/', user_views.register, name='register'),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('', include('pages.urls')),
    path('products/', include('products.urls')),
)

if settings.DEBUG:
    # Add debug-toolbar
    import debug_toolbar  # noqa
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))

    # Serve media files through Django.
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    # Show error pages during development
    urlpatterns += [
        url(r'^403/$', permission_denied),
        url(r'^404/$', page_not_found),
        url(r'^500/$', server_error)
    ]
