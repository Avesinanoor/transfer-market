from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from main.models import Player
from main.forms import PlayerForm


# Create your views here.

def show_main(request):
    player_list = Player.objects.all()

    context = {
        'npm': '2406405720',  # Ganti dengan NPM kamu
        'name': 'Daffa Abhinaya',  # Ganti dengan nama kamu
        'class': 'PBP C',  # Ganti dengan kelas kamu
        'aplikasi': 'Transfer Market',
        'player_list': player_list
    }
    return render(request, 'main.html', context)

def register_player(request):
    form = PlayerForm(request.POST or None)
    
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')
    context = {
        'form': form,}
    return render(request, 'register_player.html', context)

def show_player(request, id):
    player = get_object_or_404(Player, pk=id)
    context = {
        'player': player,
    }
    return render(request, 'player_detail.html', context)

def delete_player(request, id):
    player = get_object_or_404(Player, pk=id)
    player.delete()
    messages.success(request, f'Player {player} deleted successfully.')
    return redirect('main:show_main')

def show_xml(request):
    players_list = Player.objects.all()
    xml_data = serializers.serialize('xml', players_list)
    return HttpResponse(xml_data, content_type='application/xml')

def show_json(request):
    players_list = Player.objects.all()
    json_data = serializers.serialize('json', players_list)
    return HttpResponse(json_data, content_type='application/json') 

def show_xml_by_id(request, player_id):
    try:
        player_item = Player.objects.get(pk=player_id)
        xml_data = serializers.serialize('xml', player_item)
        return HttpResponse(xml_data, content_type='application/xml')
    except Player.DoesNotExist:
        return HttpResponse(status=404)

def show_json_by_id(request, player_id):
    try:
        player_item = Player.objects.get(pk=player_id)
        json_data = serializers.serialize('json', [player_item])
        return HttpResponse(json_data, content_type='application/json')
    except Player.DoesNotExist:
        return HttpResponse(status=404)