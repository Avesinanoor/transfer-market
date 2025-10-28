from django.urls import path
from main.views import (
    show_main, register_player, show_player, delete_player, 
    show_json, show_xml, show_json_by_id, show_xml_by_id,
    register, login_user, logout_user, edit_player,
    get_players_json, create_player_ajax, update_player_ajax, 
    delete_player_ajax, register_ajax, login_ajax, logout_ajax
)

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register-player/', register_player, name='register_player'),
    path('player/<str:id>/', show_player, name='show_player'),
    path('delete-player/<str:id>/', delete_player, name='delete_player'),
    path('edit/<uuid:id>/edit', edit_player, name='edit_player'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:player_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:player_id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    
    # AJAX endpoints
    path('api/players/', get_players_json, name='get_players_json'),
    path('api/players/create/', create_player_ajax, name='create_player_ajax'),
    path('api/players/<str:id>/update/', update_player_ajax, name='update_player_ajax'),
    path('api/players/<str:id>/delete/', delete_player_ajax, name='delete_player_ajax'),
    path('api/register/', register_ajax, name='register_ajax'),
    path('api/login/', login_ajax, name='login_ajax'),
    path('api/logout/', logout_ajax, name='logout_ajax'),
]