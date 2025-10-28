from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from main.models import Player
from main.forms import PlayerForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

# Create your views here.

@login_required(login_url='/login')
def show_main(request):
    context = {
        'npm': '2406405720',
        'name': request.user.username,
        'class': 'PBP C',
        'aplikasi': 'Transfer Market',
        'last_login': request.COOKIES.get('last_login', 'Never')
    }
    return render(request, 'main.html', context)

def register_player(request):
    form = PlayerForm(request.POST or None)
    
    if form.is_valid() and request.method == 'POST':
        player_entry = form.save(commit=False)
        player_entry.user = request.user
        player_entry.save()
        return redirect('main:show_main')
    
    context = {
        'form': form,}
    
    return render(request, 'register_player.html', context)

@login_required(login_url='/login')
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

def edit_player(request, id):
    news = get_object_or_404(Player, pk=id)
    form = PlayerForm(request.POST or None, instance=news)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_player.html", context)

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
        player_item = Player.objects.filter(pk=player_id)
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
    
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

# AJAX Views
@login_required(login_url='/login')
def get_players_json(request):
    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'all':
        players = Player.objects.all()
    else:
        players = Player.objects.filter(user=request.user)
    
    data = []
    for player in players:
        data.append({
            'id': str(player.id),
            'name': player.name,
            'price': player.price,
            'description': player.description,
            'thumbnail': player.thumbnail or '',
            'category': player.category,
            'category_display': player.get_category_display(),
            'is_featured': player.is_featured,
            'club': player.club,
            'nationality': player.nationality,
            'height': player.height,
            'user_id': player.user.id,
            'is_owner': player.user.id == request.user.id
        })
    
    return JsonResponse({'players': data})

@login_required(login_url='/login')
@require_POST
def create_player_ajax(request):
    try:
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        thumbnail = request.POST.get('thumbnail')
        category = request.POST.get('category')
        is_featured = request.POST.get('is_featured') == 'true'
        club = request.POST.get('club')
        nationality = request.POST.get('nationality')
        height = request.POST.get('height')
        
        player = Player.objects.create(
            user=request.user,
            name=name,
            price=price,
            description=description,
            thumbnail=thumbnail if thumbnail else None,
            category=category,
            is_featured=is_featured,
            club=club,
            nationality=nationality,
            height=height
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Player created successfully!',
            'player': {
                'id': str(player.id),
                'name': player.name,
                'price': player.price
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required(login_url='/login')
@require_POST
def update_player_ajax(request, id):
    try:
        player = get_object_or_404(Player, pk=id, user=request.user)
        
        player.name = request.POST.get('name')
        player.price = request.POST.get('price')
        player.description = request.POST.get('description')
        player.thumbnail = request.POST.get('thumbnail') if request.POST.get('thumbnail') else None
        player.category = request.POST.get('category')
        player.is_featured = request.POST.get('is_featured') == 'true'
        player.club = request.POST.get('club')
        player.nationality = request.POST.get('nationality')
        player.height = request.POST.get('height')
        
        player.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Player updated successfully!',
            'player': {
                'id': str(player.id),
                'name': player.name,
                'price': player.price
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required(login_url='/login')
@require_POST
def delete_player_ajax(request, id):
    try:
        player = get_object_or_404(Player, pk=id, user=request.user)
        player_name = player.name
        player.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Player {player_name} deleted successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@csrf_exempt
def register_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password1 = data.get('password1')
            password2 = data.get('password2')
            
            if password1 != password2:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Passwords do not match!'
                }, status=400)
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Username already exists!'
                }, status=400)
            
            user = User.objects.create_user(username=username, password=password1)
            user.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Account created successfully!'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

@csrf_exempt
def login_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'status': 'success',
                    'message': 'Login successful!',
                    'username': user.username
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid username or password!'
                }, status=401)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

@login_required(login_url='/login')
def logout_ajax(request):
    logout(request)
    return JsonResponse({
        'status': 'success',
        'message': 'Logged out successfully!'
    })
