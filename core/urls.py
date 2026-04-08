from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap as wagtail_sitemap
from .sitemaps import WeekSitemap, ResultsSitemap, FixturesSitemap, StaticPagesSitemap, BlogSitemap

sitemaps = {
    'weeks': WeekSitemap,
    'results': ResultsSitemap,
    'fixtures': FixturesSitemap,
    'static': StaticPagesSitemap,
    'blog': BlogSitemap,
}

urlpatterns = [
    # Django admin
    path('django-admin/', admin.site.urls),

    # Wagtail CMS admin
    path('admin/', include(wagtailadmin_urls)),

    # Pool app (fixtures, results, predictions)
    path('', include('pool.urls')),
    
    path('', include('accounts.urls')),

    # Blog app
    # path('blog/', include('blog.urls')),

    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),

    # Wagtail pages (Contact, About, Disclaimer etc.) — must be last
    path('', include(wagtail_urls)),
    
    

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)