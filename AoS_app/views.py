from django.http import HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic.edit import CreateView, BaseCreateView
from django.views.generic import ListView, DetailView
from AoS_app.models import Tournament, Player, Game, TournamentPlayer, GamePlayer, Round
from AoS_app.forms import TournamentPlayerCreateForm, PlayerCreateForm, TournamentPlayer, GamePlayerCreateForm, \
    AddPlayerToTournamentForm, TournamentPlayerEditForm, TournamentCreateForm, GameResultForm


class TournamentCreateView(View):
    def get(self, request):
        form = TournamentCreateForm()
        tournaments = Tournament.objects.all()
        return render(request, "forms.html", {"form": form, "tournaments": tournaments})

    def post(self, request):
        form = TournamentCreateForm(request.POST)
        tournaments = Tournament.objects.all()
        if form.is_valid():
            name = form.cleaned_data["name"]
            nr_of_rounds = form.cleaned_data["nr_of_rounds"]
            tournament = Tournament.objects.create(name=name, nr_of_rounds=nr_of_rounds)
            tournament.save()
        return render(request, "forms.html", {"tournaments": tournaments, "form": form})


class ShowTournaments(ListView):
    model = Tournament
    paginate_by = 20
    template_name = 'list_view.html'


class ShowPlayersView(ListView):
    model = Player
    template_name = 'show_players.html'
    fields = '__all__'


class PlayersDetailView(DetailView):
    template_name = 'player_detail.html'
    model = Player


class GameCreateView(CreateView):
    model = Game
    template_name = 'create_template.html'
    fields = '__all__'
    success_url = '/games'


class ShowGamesView(ListView):
    model = Game
    template_name = 'show_games.html'
    fields = '__all__'


class TournamentPlayerCreateView(View):
    def get(self, request, id):
        form = TournamentPlayerCreateForm()
        tournament_players = TournamentPlayer.objects.filter(tournament=id)
        return render(request, "forms.html", {"form": form, "tournament_players":tournament_players})

    def post(self, request, id):
        form = TournamentPlayerCreateForm(request.POST)
        tournament_players = TournamentPlayer.objects.filter(tournament=id)
        if form.is_valid():
            player = form.cleaned_data["player"]
            army = form.cleaned_data["army"]
            roster = form.cleaned_data["roster"]
            tournament = form.cleaned_data["tournament"]
            tournament_player = TournamentPlayer.objects.create(player=player, army=army, roster=roster, tournament=tournament)
            tournament_player.save()
        return render(request, "forms.html", {"tournament_player": tournament_player, "form": form, "tournament_players":tournament_players})


class PlayerCreateView(View):
    def get(self, request):
        form = PlayerCreateForm()
        players = Player.objects.all()
        return render(request, "forms.html", {"form": form, "players": players})

    def post(self, request):
        form = PlayerCreateForm(request.POST)
        players = Player.objects.all()
        if form.is_valid():
            name = form.cleaned_data["name"]
            last_name = form.cleaned_data["last_name"]
            nick = form.cleaned_data["nick"]
            player = Player.objects.create(name=name, last_name=last_name, nick=nick)
            player.save()
        return render(request, "forms.html", {"players": players, "form": form})


class RoundView(View):
    def get(self, request, round_pk):
        round = Round.objects.get(pk=round_pk)
        games = Game.objects.filter(round_id=round_pk)
        return render(request, "round.html", context={"round": round, "games": games, "round_pk": round_pk})

    def post(self, request, round_pk):
        round = Round.objects.get(pk=round_pk)
        games = Game.objects.filter(id=round.id)
        return render(request, "round.html", context={"round": round, "games": games, "round_pk": round_pk})


class GamePlayerCreateView(View):
    def get(self, request):
        form = GamePlayerCreateForm()
        game_players = GamePlayer.objects.filter()
        return render(request, "forms.html", {"form": form, "game_players": game_players})

    def post(self, request):
        form = GamePlayerCreateForm(request.POST)
        game_players = GamePlayer.objects.filter()
        if form.is_valid():
            player = form.cleaned_data["player"]
            kill_points = form.cleaned_data["kill_points"]
            scenario_points = form.cleaned_data["scenario_points"]
            agenda = form.cleaned_data["agenda"]
            victory_points = form.cleaned_data["victory_points"]
            game_player = GamePlayer.objects.create(player=player, kill_points=kill_points, scenario_points=scenario_points,
                                           agenda=agenda, victory_points=victory_points)
            game_player.save()
        return render(request, "forms.html", {"game_players": game_players, "form": form})


class TournamentDetailView(View):
    def get(self, request, pk):
        tournament = Tournament.objects.get(pk=pk)
        rounds = Round.objects.filter(tournament=pk)
        tournament_players = TournamentPlayer.objects.filter(tournament=pk)
        player_form = AddPlayerToTournamentForm(instance=tournament)
        return render(request, "tournament_detail.html", {"rounds":rounds,  'player_form':player_form, 'tournament':tournament, "tournament_players":tournament_players})

    def post(self, request, pk):
        tournament = Tournament.objects.get(pk=pk)
        rounds = Round.objects.filter(tournament=tournament)
        tournament_players = TournamentPlayer.objects.filter(tournament=pk)
        player_form = AddPlayerToTournamentForm(request.POST, instance=tournament)
        if player_form.is_valid():
            player_form.save()
        return render(request, "tournament_detail.html", {"rounds":rounds,  'player_form':player_form, "tournament_players":tournament_players})


class TournamentPlayerEditView(View):
    def get(self, request, id):
        tournament_player = TournamentPlayer.objects.get(pk=id)
        tournament = tournament_player.tournament.id
        form = TournamentPlayerEditForm(instance=tournament_player)
        return render(request, "forms.html", {"form":form, "tournament_player":tournament_player, "tournament":tournament})

    def post(self, request, id):
        tournament_player = TournamentPlayer.objects.get(pk=id)
        tournament = tournament_player.tournament.id
        form = TournamentPlayerEditForm(request.POST, instance=tournament_player)
        if form.is_valid():
            form.save()
        return render(request, "forms.html", {"form": form,"tournament_player":tournament_player, "tournament":tournament})


def generate_games_for_round(request, round_id):
    round = Round.objects.get(pk=round_id)
    round.generate_Tables()
    return redirect(f"/round/{round_id}")


class MainView(View):
    def get(self, request):
        playerbase = Player.objects.all()
        tournaments = Tournament.objects.all()
        return render(request, "main.html", {"playerbase":playerbase, "tournaments":tournaments})


class GameResultView(View):
    def get(self, request, id):
        game = Game.objects.get(pk=id)
        p1 = game.player_1
        p2 = game.player_2
        round = Round.objects.get(id=game.round_id)
        form = GameResultForm(initial=({"p1":p1,"p2":p2}))
        return render(request, "forms.html", {"form": form, "p1":p1, "p2":p2, "round":round})

    def post(self, request, id):
        game = Game.objects.get(pk=id)
        p1 = game.player_1
        p2 = game.player_2
        round = Round.objects.get(id=game.round_id)
        form = GameResultForm(request.POST)
        if form.is_valid():
            p1 = form.cleaned_data["p1"]
            p1.kill_points = form.cleaned_data["p1_kill_points"]
            p1.scenario_points = form.cleaned_data["p1_scenario_points"]
            p1.agenda = form.cleaned_data["p1_agenda"]
            p1.victory_points = form.cleaned_data["p1_victory_points"]
            p1.save()
            p2 = form.cleaned_data["p2"]
            p2.kill_points = form.cleaned_data["p2_kill_points"]
            p2.scenario_points = form.cleaned_data["p2_scenario_points"]
            p2.agenda = form.cleaned_data["p2_agenda"]
            p2.victory_points = form.cleaned_data["p2_victory_points"]
            p2.save()
        return redirect(f"/round/{round.id}", {"form": form, "p1": p1, "p2": p2, "round":round})


class TournamentResultView(View):
    def get(self, request, pk):
        tournament = Tournament.objects.get(pk=pk)
        results = TournamentPlayer.objects.filter(tournament=pk).order_by("-victory_points", "-kill_points")
        results = results.exclude(player__nick__contains="Dummy")
        print(results)
        return render(request, "results.html", {"results": results, "pk":pk, "tournament":tournament})










