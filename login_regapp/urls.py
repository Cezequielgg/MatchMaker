from django.urls import path
from . import views

urlpatterns = [
    path('',views.regandlogin),
    path('registration',views.registration),     
    path('login',views.login),
    path('logout',views.logout), 
    path('pass',views.inpage),  
    path('duel/<int:id>',views.duel), 
    path('duel_elo',views.duel_elo),
    path('rank_region',views.Rank_region),    
    path('delete/<int:id>',views.delete)
]