from django.forms import ModelForm
from main.models import Player

class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'price', 'description', 'thumbnail', 'category', 'is_featured', 'club', 'nationality', 'height']
