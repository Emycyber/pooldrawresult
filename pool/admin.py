from django.contrib import admin
from .models import Week, Match, Team, League
from .models import FooterLink



class MatchInline(admin.TabularInline):
    model = Match
    extra = 0
    show_change_link = True
    fields = ['match_number', 'home_team', 'away_team', 'home_score', 'away_score', 'day', 'status', 'prediction']

@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    list_display = ['number', 'season', 'date']
    inlines = [MatchInline]


# No @admin.register(Match) — removes it from the sidebar entirely
# But we still need MatchAdmin for the edit page when "Change" is clicked
class MatchAdmin(admin.ModelAdmin):
    fields = [
        'week',
        'match_number',
        ('home_team', 'away_team'),
        ('home_score', 'away_score'),
        ('league', 'day'),
        ('status', 'prediction'),
    ]

admin.site.register(Match, MatchAdmin)  # ← registered but won't appear in sidebar


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    
    
    
@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'order', 'is_active', 'opens_in_new_tab']
    list_filter = ['is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'url']