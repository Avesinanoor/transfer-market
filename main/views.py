from django.shortcuts import render

# Create your views here.

def show_main(request):
    context = {
        'npm': '2406405720',  # Ganti dengan NPM kamu
        'name': 'Daffa Abhinaya',  # Ganti dengan nama kamu
        'class': 'PBP C',  # Ganti dengan kelas kamu
        'aplikasi': 'Transfer Market'
    }
    return render(request, 'main.html', context)