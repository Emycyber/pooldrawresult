from django.contrib import admin
from .models import Week, Match, Team, League, FooterLink


class MatchInline(admin.TabularInline):
    model = Match
    extra = 0
    show_change_link = True
    autocomplete_fields = ['home_team', 'away_team', 'league']  # ← autocomplete
    fields = ['match_number', 'home_team', 'away_team', 'home_score', 'away_score', 'day', 'status', 'prediction']


@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    list_display = ['number', 'season', 'date', 'is_current', 'is_current_fixture']
    list_editable = ['is_current', 'is_current_fixture']
    inlines = [MatchInline]


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    autocomplete_fields = ['home_team', 'away_team', 'league']  # ← autocomplete
    fields = [
        'week',
        'match_number',
        ('home_team', 'away_team'),
        ('home_score', 'away_score'),
        ('league', 'day'),
        ('status', 'prediction'),
    ]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']  # ← required for autocomplete to work


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    search_fields = ['name', 'country']  # ← required for autocomplete to work


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'order', 'is_active', 'opens_in_new_tab']
    list_filter = ['is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'url']