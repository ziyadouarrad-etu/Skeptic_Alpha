from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),          # The main page
    path('solve/', views.solve_engineering_view, name='solve'), # The AJAX endpoint for the Auditor
    path('analytics/', views.analytics_dashboard, name='analytics') # The analytics dashboard
]