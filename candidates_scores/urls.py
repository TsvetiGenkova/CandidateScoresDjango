
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='candidates_scores_home'),
    path('candidates/', views.candidates, name='candidates_scores'),
]