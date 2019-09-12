from django.contrib import admin
from django.urls import path
from AoS_app import views
from django.views.generic.base import TemplateView

from AoS_app.views import TournamentPlayerCreateView, PlayerCreateView, TournamentPlayerEditView, RoundView, \
    generate_games_for_round, MainView, TournamentCreateView, GameResultView, TournamentResultView, ArmyCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view()),
    path('add_tournament/', TournamentCreateView.as_view()),
    path('tournaments/', views.ShowTournaments.as_view()),
    path('tournament/<int:pk>', views.TournamentDetailView.as_view()),
    path('add_player/', PlayerCreateView.as_view(), name="player_create"),
    path('players/', views.ShowPlayersView.as_view(), name="players"),
    path('games/', views.ShowGamesView.as_view()),
    path('add_game/', views.GameCreateView.as_view()),
    path('player/<int:pk>/', views.PlayersDetailView.as_view()),
    path('tournament/<int:tournament_pk>/round/<int:pk>/add_game/', views.GameCreateView.as_view()),
    path('add_game_player/', views.GamePlayerCreateView.as_view()),
    path('add_tournament_player/<int:id>', TournamentPlayerCreateView.as_view(), name="add_tournament_player"),
    path('edit_tournament_player/<int:id>', TournamentPlayerEditView.as_view(), name="edit_tournament_player"),
    path('generate_table/<int:round_id>', generate_games_for_round),
    path('round/<int:round_pk>', RoundView.as_view()),
    path('game/<int:id>', GameResultView.as_view()),
    path('results/<int:pk>', TournamentResultView.as_view()),
    path('add_army/', ArmyCreateView.as_view())
]