from django.urls import path
from main.views import show_main, register_player, show_player, delete_player, show_json, show_xml, show_json_by_id, show_xml_by_id
from main.views import register, login_user, logout_user, edit_player
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

]