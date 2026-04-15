from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import F
from django.contrib.auth.models import User
from blog.models import BlogPage
from .models import Match, Week
import os


def get_week(week_number=None):
    if week_number is None:
        return Week.objects.order_by('-number').first()
    return get_object_or_404(Week, number=week_number)


def home(request, week_number=None):
    current_week = get_week(week_number)

    if current_week is None:
        return render(request, 'pool/index.html', {'no_data': True})

    weeks = Week.objects.order_by('-number')
    matches = (
        Match.objects
        .filter(week=current_week)
        .select_related('home_team', 'away_team', 'league')
        .order_by('match_number')
    )
    draw_count = matches.filter(
        home_score__isnull=False,
        away_score__isnull=False,
        home_score=F('away_score')
    ).count()

    previous_week = Week.objects.filter(number__lt=current_week.number).order_by('-number').first()
    next_week = Week.objects.filter(number__gt=current_week.number).order_by('number').first()
    
    latest_posts = BlogPage.objects.live().public().order_by('-date')[:3]


    return render(request, 'pool/index.html', {
        'week': current_week,
        'weeks': weeks,
        'matches': matches,
        'draw_count': draw_count,
        'previous_week': previous_week,
        'next_week': next_week,
        'latest_posts': latest_posts,
    })


def predictions(request, week_number=None):
    current_week = get_week(week_number)

    if current_week is None:
        return render(request, 'pool/predictions.html', {'no_data': True})

    weeks = Week.objects.order_by('-number')
    matches = (
        Match.objects
        .filter(week=current_week)
        .select_related('home_team', 'away_team', 'league')
        .order_by('match_number')
    )

    return render(request, 'pool/predictions.html', {
        'week': current_week,
        'weeks': weeks,
        'matches': matches,
    })


def about(request):
    return render(request, 'pool/about.html')


def contact(request):
    return render(request, 'pool/contact.html')


def disclaimer(request):
    return render(request, 'pool/disclaimer.html')


def partners(request):
    return render(request, 'pool/partners.html')


def advertise(request):
    return render(request, 'pool/advertise.html')


def results(request, week_number=None):
    current_week = get_week(week_number)

    if current_week is None:
        return render(request, 'pool/results.html', {'no_data': True})

    weeks = Week.objects.order_by('-number')
    matches = (
        Match.objects
        .filter(week=current_week)
        .select_related('home_team', 'away_team', 'league')
        .order_by('match_number')
    )
    draw_count = matches.filter(
        home_score__isnull=False,
        away_score__isnull=False,
        home_score=F('away_score')
    ).count()
    has_live_matches = matches.filter(status='live').exists()

    previous_week = Week.objects.filter(number__lt=current_week.number).order_by('-number').first()
    next_week = Week.objects.filter(number__gt=current_week.number).order_by('number').first()

    return render(request, 'pool/results.html', {
        'week': current_week,
        'weeks': weeks,
        'matches': matches,
        'draw_count': draw_count,
        'previous_week': previous_week,
        'next_week': next_week,
        'has_live_matches': has_live_matches,
    })


def fixtures(request, week_number=None):
    current_week = get_week(week_number)

    if current_week is None:
        return render(request, 'pool/fixtures.html', {'no_data': True})

    weeks = Week.objects.order_by('-number')
    matches = (
        Match.objects
        .filter(week=current_week, status='fixture')
        .select_related('home_team', 'away_team', 'league')
        .order_by('match_number')
    )

    previous_week = Week.objects.filter(number__lt=current_week.number).order_by('-number').first()
    next_week = Week.objects.filter(number__gt=current_week.number).order_by('number').first()

    return render(request, 'pool/fixtures.html', {
        'week': current_week,
        'weeks': weeks,
        'matches': matches,
        'previous_week': previous_week,
        'next_week': next_week,
    })


def archive(request):
    weeks = Week.objects.all().order_by('-number')
    return render(request, 'pool/archive.html', {'weeks': weeks})



def robots_txt(request):
    content = """User-agent: *
    Allow: /
    Disallow: /admin/
    Disallow: /django-admin/
    Disallow: /vip/
    Disallow: /dashboard/

    Sitemap: https://pooldrawresult.com/sitemap.xml
    """
    return HttpResponse(content, content_type='text/plain')



def check_cloudinary(request):
    import os
    data = {
        'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', 'NOT SET'),
        'API_KEY': os.environ.get('CLOUDINARY_API_KEY', 'NOT SET'),
        'API_SECRET': 'SET' if os.environ.get('CLOUDINARY_API_SECRET') else 'NOT SET',
        'DEFAULT_FILE_STORAGE': getattr(__import__('django.conf', fromlist=['settings']).settings, 'DEFAULT_FILE_STORAGE', 'NOT SET'),
    }
    from django.http import JsonResponse
    return JsonResponse(data)