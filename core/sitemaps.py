from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from pool.models import Week
from blog.models import BlogPage


class WeekSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Week.objects.all().order_by('-number')

    def location(self, obj):
        return f'/week/{obj.number}/'

    def lastmod(self, obj):
        return obj.date


class ResultsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Week.objects.all().order_by('-number')

    def location(self, obj):
        return f'/results/week/{obj.number}/'

    def lastmod(self, obj):
        return obj.date


class FixturesSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Week.objects.all().order_by('-number')

    def location(self, obj):
        return f'/fixtures/week/{obj.number}/'

    def lastmod(self, obj):
        return obj.date


class StaticPagesSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return [
            'pool:home',
            'pool:results',
            'pool:fixtures',
            'pool:predictions',
            'pool:archive',
            'pool:about',
            'pool:contact',
            'pool:disclaimer',
            'pool:partners',
            'pool:advertise',
        ]

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return BlogPage.objects.live().public().order_by('-date')

    def location(self, obj):
        return obj.full_url

    def lastmod(self, obj):
        return obj.last_published_at