from django.urls import path
from . import views

app_name = 'pool'

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    path('week/<int:week_number>/', views.home, name='week_view'),

    # Results
    path('results/', views.results, name='results'),
    path('results/week/<int:week_number>/', views.results, name='results_week'),

    # Fixtures
    path('fixtures/', views.fixtures, name='fixtures'),
    path('fixtures/week/<int:week_number>/', views.fixtures, name='fixtures_week'),

    # Predictions
    path('predictions/', views.predictions, name='predictions'),
    path('predictions/week/<int:week_number>/', views.predictions, name='predictions_week'),

    # Archive
    path('archive/', views.archive, name='archive'),

    # Static pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),
    path('partners/', views.partners, name='partners'),
    path('advertise/', views.advertise, name='advertise'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    
    
    path('setup-admin/', views.create_admin, name='create_admin'),
]