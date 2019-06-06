from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q

from .models import Player, Game
from .constants import *

# player dashboard view
def index(request):
    player = request.player
    context = {
        'player': player,
        'other_new_games': Game.objects.filter(~Q(player_a=player.id)),
        'own_games': player.own_games.all()
    }
    return render(request, 'game/index.html', context=context)


# login form view
def login(request):
    if(request.player):
        return HttpResponseRedirect(reverse('game:index'))
    return render(request, 'game/login.html')


# login form action
def enter(request):
    # get name from form
    name = request.POST['name']
    # if name exists try to get player or create a new one
    if(name):
        try:
            player = Player.objects.get(name=name)
        except Player.DoesNotExist:
            player = Player(name=name)
            player.save()
        # save player id in session
        request.session['player_id'] = player.id
    # redirect to game index
    return HttpResponseRedirect(reverse('game:index'))


# logout form action
def leave(request):
    # remove info from session if exists
    if('player_id' in request.session):
        del request.session['player_id']
    # redirect to game index
    return HttpResponseRedirect(reverse('game:index'))


# new game action
def new(request):
    game = Game(player_a=request.player, steps='[]')
    game.save()
    return HttpResponseRedirect(reverse('game:index'))


# game field view
def field(request):
    context = {
        'player': request.player
    }
    return render(request, 'game/field.html', context=context)