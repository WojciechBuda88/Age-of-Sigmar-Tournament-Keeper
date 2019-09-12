from django.db import models
import math
import random


class Tournament(models.Model):
    name = models.CharField(max_length=255)
    nr_of_rounds = models.IntegerField()
    players = models.ManyToManyField('Player', through='TournamentPlayer')

    def save(self, *args, **kwargs):
        id = self.id
        super().save(*args, **kwargs)
        if id is None:
            for i in range(self.nr_of_rounds, 0, -1):
                Round.objects.create(name=i, nr=i, tournament=self)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    nick = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.nick


class Round(models.Model):
    name = models.CharField(max_length=128)
    nr = models.IntegerField()
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING)

    def generate_Tables(self):

        if self.game_set.all().count() > 0:
            return
        players = self.generate_list_of_players()
        count = 1
        while len(players) > 1:
            g1 = GamePlayer(player=players.pop(0))
            g1.save()
            g2 = GamePlayer(player=players.pop(0))
            g2.save()
            Game.objects.create(table=count, round=self, player_1=g1, player_2=g2)
            count +=1
        if len(players) == 1:
            g1 = GamePlayer(player=players.pop(0))
            g1.save()
            Game.objects.create(table=count, round=self, player_1=g1, player_2=None)

    def generate_list_of_players(self):

        if self.nr == 1:
            players = list(self.tournament.players.all())
            random.shuffle(players)
            return players
        else:
            tplayers = TournamentPlayer.objects.filter(tournament=self.tournament).order_by('-victory_points', '-kill_points')
            players = [x.player for x in tplayers]
            return players

    def __str__(self):
        return self.name


class GamePlayer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    kill_points = models.IntegerField(null=True, default=0)
    scenario_points = models.IntegerField(null=True,default=0)
    agenda = models.BooleanField(default=False)
    victory_points = models.IntegerField(null=True, default=0)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.id is not None:
            if hasattr(self, 'player_1'):
                game = self.player_1
            else:
                game = self.player_2
            tournament = game.round.tournament
            tplayer = TournamentPlayer.objects.get(tournament=tournament, player=self.player)
            tplayer.kill_points += self.kill_points
            tplayer.victory_points += self.victory_points
            tplayer.save()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.player.nick


class Game(models.Model):
    table = models.IntegerField()
    round = models.ForeignKey(Round, on_delete=models.DO_NOTHING)
    player_1 = models.OneToOneField(GamePlayer, related_name='player_1', on_delete=models.DO_NOTHING, null=True)
    player_2 = models.OneToOneField(GamePlayer, related_name='player_2', on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f"{self.player_1} vs {self.player_2} w {self.round} rundzie"


class Army(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class TournamentPlayer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    army = models.ForeignKey(Army, on_delete=models.DO_NOTHING, null=True)
    roster = models.TextField(null=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING)
    kill_points = models.IntegerField(default=0)
    victory_points = models.IntegerField(default=0)

    def __str__(self):
        return self.player.nick