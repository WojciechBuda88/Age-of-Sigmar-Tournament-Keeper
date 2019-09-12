from django.forms import ModelForm
from django import forms
from AoS_app.models import TournamentPlayer, Player, GamePlayer, Tournament


class TournamentPlayerCreateForm(ModelForm):
    class Meta:
        model = TournamentPlayer
        exclude = ["tournament"]


class AddPlayerToTournamentForm(ModelForm):

    class Meta:
        model = Tournament
        fields = ['players']
        widgets = {'players':forms.CheckboxSelectMultiple}


class PlayerCreateForm(ModelForm):
    class Meta:
        model = Player
        fields = "__all__"


class GamePlayerCreateForm(ModelForm):
    class Meta:
        model = GamePlayer
        fields = "__all__"


class TournamentPlayerEditForm(ModelForm):
    class Meta:
        model = TournamentPlayer
        exclude = ["tournament", "player"]


class TournamentCreateForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ["name", "nr_of_rounds"]


class GameResultForm(forms.Form):
    p1 = forms.ModelChoiceField(queryset=GamePlayer.objects.all())
    p1_kill_points = forms.IntegerField()
    p1_scenario_points = forms.IntegerField()
    p1_agenda = forms.BooleanField(required=False)
    p1_victory_points = forms.IntegerField()
    p2 = forms.ModelChoiceField(queryset=GamePlayer.objects.all())
    p2_kill_points = forms.IntegerField()
    p2_scenario_points = forms.IntegerField()
    p2_agenda = forms.BooleanField(required=False)
    p2_victory_points = forms.IntegerField()



