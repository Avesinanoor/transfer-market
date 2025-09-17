<details>
<summary> Tugas 2 </summary>

### Link PWS: https://pbp.cs.ui.ac.id/web/project/daffa.abhinaya/transfermarket

# 1. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step.
## Membuat Proyek Django Baru
###  Instalasi dan Inisiasi Django
- Membuat direktori proyek dengan menggunakan code berikut di command prompt
```
mkdir transfer-market
cd transfer-market
```
- Mengaktifkan virtual environment
```
python -m venv env           
env\Scripts\activate         
```

- Membuat requirements.txt di direktori tersebut yang berisi dependencies
```
django
gunicorn
whitenoise
psycopg2-binary
requests
urllib3
python-dotenv
```
```
pip install -r requirements.txt
```
- Buat file .env dan .env.prod yang berisi database pribadi, settings environment

```
#env
PRODUCTION = False
```
```
#.env.prod
#kredensial database berdasarkan email yang sudah diberikan
SCHEMA=tugas_individu
PRODUCTION=True
```
- Konfigurasi settings.py untuk nanti mengambil info database dari .env.prod dan menambahkan allowed host
```
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
...
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
...
PRODUCTION = os.getenv('PRODUCTION', 'False').lower() == 'true'
...
# Database configuration
if PRODUCTION:
    # Production: gunakan PostgreSQL dengan kredensial dari environment variables
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
            'OPTIONS': {
                'options': f"-c search_path={os.getenv('SCHEMA', 'public')}"
            }
        }
    }
else:
    # Development: gunakan SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```
- Migrasi database dan run server
```
python manage.py migrate
python manage.py runserver
```
### Upload project ke Repo GitHub
- Buat repo baru di GitHub, transfer-market
- run code berikut untuk membuat folder .git
```
git init
```
- Buat file .gitignore supaya file-file  kredensial database dan konfigurasi tidak ikut terupload atau push ke repo GitHub
- Menghubung direktori lokal transfer-market tadi ke repo GitHub, dan set master sebagai default branch
```
git remote add origin https://github.com/Avesinanoor/transfer-market.git
```
- Upload ke repo
```
git add .
git commit -m "Instalasi dan Inisiasi Django"
git push origin master
```
### Inisiasi untuk deploy melalui PWS

- login ke https://pbp.cs.ui.ac.id. dengan SSO
- Buat proyek baru
- Simpan informasi kredensial
- Copy code yang berada di .env.prod dan paste ke Raw Editor di bagian Environs
- Menambahkan URL deploypment PWS ke ALLOWED_HOST di settings.py
- Git add, commit, push perubahan ke repo GitHub
- Run code perintah dari PWS dan masukkan kredensial dari PWS yang sudah disimpan tadi
```
git remote add pws https://pbp.cs.ui.ac.id/daffa.abhinaya/transfermarket
git branch -M master
git push pws master
```

## Membuat aplikasi Main
- Aktifkan mode virtual environment terlebih dahulu
- Run kode untuk membuat aplikasi main
```
python manage.py startapp main
```
- Menambahkan 'main' ke INSTALLED_APPS di settings.py

## Membuat model pada aplikasi main dengan nama Product

- Saya buat class Product yang berisi atribut-atribut wajib
- Tema dari aplikasi transfer market saya adalah semacam market yang berisi informasi, database, dan statistik pemain bola
- Setiap pemain bola memiliki posisinya masing-masing di lapangan seperti yang tertera di CATEGORY_CHOICES
- Setiap pemain bola juga dapat dibeli dan pindah club, "transfer", pada  "transfer window"

```python
from django.db import models

# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('goalkeeper', 'Goalkeeper'),
        ('center-back', 'Center-Back'),
        ('left-back', 'Left-Back'),
        ('right-back', 'Right-Back'),
        ('center-midfielder', 'Center-Midfielder'),
        ('attacking-midfielder', 'Attacking-Midfielder'),
        ('defensive-midfielder', 'Defensive-Midfielder'),
        ('left-winger', 'Left-Winger'),
        ('right-winger', 'Right-Winger'),
        ('striker', 'Striker'),
    ]
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_featured = models.BooleanField(default=False)
    club = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    height = models.FloatField()

    def __str__(self):
        return self.name
```
## Membuat fungsi pada views.py untuk dikembalikan ke dalam sebuah template HTML
- Menambahkan import render pada views.py di aplikasi main untuk render HTML
- Buat fungsi show_main di mana isi dari variabel-variabelnya akan dipakai untuk main.html dan ditampilkan
```python
def show_main(request):
    context = {
        'npm' : '2406405720',
        'name': 'Daffa Abhinaya',
        'class': 'PBP C'
    }
    return render(request, "main.html", context)
```
- Buat direktori template di dalam main
- Pada template buat berkas main.html yang berisi template variables berdasarkan struktur kode Django yang akan menampilkan nilai dari variabel dalam context di fungsi show_main

```html
#main.html
<h1>Nama Aplikasi: </h1>
<p> {{ aplikasi }} <p>

<h4>NPM: </h4>
<p>{{ npm }}</p> 
<h4>Name: </h4>
<p>{{ name }}</p>
<h4>Class: </h4>
<p>{{ class }}</p> 
```
## Routing pada urls.py aplikasi main untuk memetakan fungsi pada views.py.
- Buat file urls.py di dalam main dan isi
```
from django.urls import path
from main.views import show_main

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
]
```
- Pada urls.py yang di dalam transfer-market, tambah import include
- tambah rute URL untuk mengarahkan ke main
```
urlpatterns = [
    ...
    path('', include('main.urls')),
    ...
]
```
- urls.py pada aplikasi main mengatur rute URL spesifik untuk fitur-fitur dalam aplikasi tersebut.
- urls.py pada proyek transfer-market dapat mengimpor rute URL dari berkas urls.py aplikasi-aplikasi.

## Melakukan deployment ke PWS 
- Saya sudah inisiasi PWS pada tahap inisiasi Django di awal
- Push ke Repo GitHub dan PWS
```
git add .
git commit -m "aplikasi main, fungsi views.py, routing urls.py"
git push origin master
git push pws master

```
## 2. Bagan yang berisi request client ke web aplikasi berbasis Django beserta responnya dan jelaskan pada bagan tersebut kaitan antara `urls.py`, `views.py`, `models.py`, dan berkas html.
<img src= "https://learndjango.com/static/images/courses/dfb/02_django_architecture.png">
sumber: https://learndjango.com/courses/django-for-beginners/chapter-2-hello-world-website

- Request dari browser masuk ke URL Dispatcher `urls.py`, yang menyesuaikan pola URL dan memanggil view yang cocok. 

- View `views.py` menerima HttpRequest. Bisa langsung membuat respons atau mengambil/menulis data lewat Model. 

- Model `models.py` mendefinisikan struktur tabel dan logika data; lewat ORM, view melakukan query ke database lalu mendapat hasilnya. 

- View kemudian mengirim data ke Template (file HTML) untuk dirender menjadi halaman yang siap ditampilkan. 

- Hasil render dikembalikan sebagai HTTP Response ke browser. Siklus bagan ini akan berulang untuk setiap request baru.
 
## 3. Jelaskan peran `settings.py` dalam proyek Django!
#### Tempat baca environment & kunci akses
- Memuat variabel dari .env/.env.prod di awal settings.py (pakai load_dotenv()), supaya nilai seperti DB host, user, dan schema bisa dipakai tanpa tertera di settings.py

#### Mengatur host yang diizinkan (ALLOWED_HOSTS)
- Untuk pengembangan lokal, tambahkan "localhost" dan "127.0.0.1". Saat deploy ke PWS, tambahkan juga URL PWS agar situsnya bisa diakses dari domain itu. 

#### Memilih mode & database (development dan production)

- Jika PRODUCTION=True, DATABASES memakai PostgreSQL dengan kredensial dari environment variables.

- Jika PRODUCTION=False, DATABASES memakai SQLite lokal.
Semua pengaturan ini ditaruh di settings.py. 

#### Mendaftarkan aplikasi ke proyek (INSTALLED_APPS)
- Setelah membuat app main, tambah 'main' ke INSTALLED_APPS dalam settings.py untuk “mengaktifkan” app tersebut (model, template-nya ikut dikenali Django). 

#### Settings.py adalah pusat konfigurasi proyek yang memuat env vars, menentukan host yang boleh mengakses, memilih database sesuai lingkungan, dan mendaftarkan app yang digunakan sehingga proyek bisa jalan lokal dan di PWS.

## 4. Bagaimana cara kerja migrasi database di Django?
- Misalnya mulai dari membuat model pada models.py seperti 
```python
from django.db import models

# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('goalkeeper', 'Goalkeeper'),
        ('center-back', 'Center-Back'),
        ('left-back', 'Left-Back'),
        ('right-back', 'Right-Back'),
        ('center-midfielder', 'Center-Midfielder'),
        ('attacking-midfielder', 'Attacking-Midfielder'),
        ('defensive-midfielder', 'Defensive-Midfielder'),
        ('left-winger', 'Left-Winger'),
        ('right-winger', 'Right-Winger'),
        ('striker', 'Striker'),
    ]
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_featured = models.BooleanField(default=False)
    club = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    height = models.FloatField()

    def __str__(self):
        return self.name
```
- Buat migration dengan
```
python manage.py makemigrations
```
Django mendeteksi perubahan pada model dan membuat file migration (0001_initial.py) berisi operasi CreateModel
```
# Generated by Django 5.2.6 on 2025-09-09 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('goalkeeper', 'Goalkeeper'), ('center-back', 'Center-Back'), ('left-back', 'Left-Back'), ('right-back', 'Right-Back'), ('center-midfielder', 'Center-Midfielder'), ('attacking-midfielder', 'Attacking-Midfielder'), ('defensive-midfielder', 'Defensive-Midfielder'), ('left-winger', 'Left-Winger'), ('right-winger', 'Right-Winger'), ('striker', 'Striker')], max_length=20)),
                ('is_featured', models.BooleanField(default=False)),
                ('club', models.CharField(max_length=100)),
                ('nationality', models.CharField(max_length=100)),
                ('height', models.FloatField()),
            ],
        ),
    ]
```
- Menerapkan migration dengan
```
python manage.py migrate
```
Django menjalankan operasi migration ke database dan riwayat migration disimpan di `django_migrations`
- Setiap kali nanti mengedit models.py, harus melakukan migration lagi dengan step-step tadi dan Django akan membuat file migration baru lagi.


## 5. Menurut Anda, dari semua framework yang ada, mengapa framework Django dijadikan permulaan pembelajaran pengembangan perangkat lunak?
Django cocok untuk permulaan karena “batteries-included”: sudah ada URL routing, views, template engine, ORM+migrasi, autentikasi, proteksi CSRF, dan admin, jadi pemula bisa fokus ke konsep web tanpa merakit banyak library. Pola MTV-nya jelas; `urls.py` memilih view, view memproses dan (jika perlu) mengambil data lewat model, lalu merender template sehingga pemisahan tanggung jawab mudah dipahami dan ditransfer ke framework lain. Tooling yang seragam (`manage.py`, `settings.py`, pemisahan `.env` .`env.prod`, hingga deploy ke PWS) membuat setup, debugging, dan rilis jadi lebih sederhana. Django memiliki dokumentasi yang lengkap dan penggunaan Python yang sudah sangat familiar karena sudah dipelajari di DDP1.

## 6. Apakah ada feedback untuk asisten dosen tutorial 1 yang telah kamu kerjakan sebelumnya?
Menurut saya isi dan informasi tutorial 1 sudah lengkap, mudah diikuti dan informatif dengan setiap penjelasannya yang mudah dipahami. Asdos juga sudah selalu bersedia dengan stand by di voice channel server discord jika ada pertanyaan atau error.
</details>

<details>
<summary> Tugas 3 </summary>


## Jelaskan mengapa kita memerlukan data delivery dalam pengimplementasian sebuah platform?

Kita perlu data delivery karena itu cara menyalurkan data dari tempat penyimpanan ke tempat pemakaian (browser, aplikasi mobile, layanan third-party) dengan tepat waktu, akurat, aman, dan andal. Tanpa hal ini, fitur platform tidak dapat berjalan dengan baik: halaman tidak terisi, status pesanan tidak ter-update, integrasi mengalami kegagalan. Dengan pengiriman data yang terorganisir, kita dapat 
- memberikan pengalaman cepat kepada pengguna (paging, caching, minimal latensi)
- menjaga keakuratan dan sinkronisasi data antar komponen 
- mendukung banyak klien dan integrasi (REST/JSON, XML, webhook)
- melayani real-time jika diperlukan (notifikasi, tracking) 
- memastikan keandalan dan skalabilitas (retry, queue, idempotency)
- memenuhi aspek keamanan (auth, otorisasi, HTTPS). 

## Menurutmu, mana yang lebih baik antara XML dan JSON? Mengapa JSON lebih populer dibandingkan XML?
Menurutku, JSON lebih cocok karena formatnya lebih sederhana dan ringkas (payload kecil), dirancang khusus untuk pertukaran data, dan umumnya memberikan performa serta kecepatan komunikasi yang lebih baik. Itulah sebabnya JSON banyak digunakan untuk API dan aplikasi mobile.

JSON lebih populer karena sifatnya yang lebih sederhana dan padat untuk keperluan data interchange, JSON cenderung lebih cepat dalam proses dan transmisi serta lebih hemat bandwidth. Dalam praktik modern, pola ini menjadikan JSON pilihan default untuk API web dan aplikasi mobile atau penyimpanan data, sementara XML tetap relevan dalam skenario yang memang memerlukan struktur dokumen yang lebih kompleks.

## Jelaskan fungsi dari method is_valid() pada form Django dan mengapa kita membutuhkan method tersebut?
Django Form/ModelForm dipakai untuk menjalankan seluruh proses validasi atas data yang di-bind ke form dan memberi tahu apakah data itu layak dipakai/di-save.

### Fungsi `is_valid()`

Ketika  memanggilnya pada form yang sudah dibound (misal, `PlayerForm(request.POST)`):

- Mengembalikan `True` bila tidak ada error; `False` bila ada error.
- `save()` (ModelForm) — menyimpan data form yang valid menjadi objek model baru. 
- `redirect()` — mengarahkan pengguna kembali (misal ke halaman daftar) setelah save(). 
- `get_object_or_404() `— mengambil satu objek berdasarkan pk; jika tidak ada, kembalikan 404 (dipakai di detail). 
- `{{ form.as_table }}` (rendering form di template) dan `{% csrf_token %}` untuk proteksi CSRF saat submit. 


### Mengapa kita membutuhkannya?

- Menjaga integritas data sebelum menyentuh database (mencegah ProgrammingError/constraint error).
- Untuk mengecek apakah data yang dimasukkan pada form memenuhi aturan yang ditetapkan di model dan ketentuan validasi Django.
- Umpan balik ke pengguna lewat form.errors.
- Keamanan & ketahanan: menolak input tak valid lebih awal.

## Mengapa kita membutuhkan csrf_token saat membuat form di Django? Apa yang dapat terjadi jika kita tidak menambahkan csrf_token pada form Django? Bagaimana hal tersebut dapat dimanfaatkan oleh penyerang?
###  Mengapa butuh `csrf_token`
Untuk mencegah Cross-Site Request Forgery (CSRF): serangan yang “meminjam” sesi login pengguna agar browser mereka mengirim aksi tanpa sadar (misal membuat/menghapus data) ke situs kita. Django mencegah ini dengan token rahasia: server menaruh CSRF cookie dan mewajibkan hidden field `csrfmiddlewaretoken` di setiap form POST internal; server hanya menerima request jika token pada form cocok dengan cookie.

### Apa yang terjadi jika tidak menambahkan `csrf_token`
- Secara default, Django memblokir request POST (HTTP 403) karena gagal verifikasi CSRF. 
Django Project
- Jika verifikasi dinonaktifkan/diabaikan, menjadi rentan CSRF: penyerang bisa memicu aksi di akun korban (misal submit form, ubah profil, hapus data).

### Bagaimana penyerang memanfaatkannya
Penyerang membuat halaman yang auto-submit form POST ke endpoint kita (misal pada `urls.py` di bagian `player<id>register-player/`) dengan parameter pilihan mereka. Saat korban sedang login, browser otomatis menyertakan session cookie; tanpa validasi token, server mengira request itu sah dan mengeksekusi aksi tersebut. 

## Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).

### Tambahkan 4 fungsi views baru untuk melihat objek yang sudah ditambahkan dalam format XML, JSON, XML by ID, dan JSON by ID.

#### Pada `views.py` di direktori  main
Import:
- `HttpResponse` untuk mengirim respons HTTP,
- `serializers` untuk mengubah QuerySet/objek model menjadi teks XML/JSON.
```python
from django.http import HttpResponse 
from django.core import serializers
```
Kemudian menambahkan 4 fungsi untuk melihat objek dalam format XML, JSON, XML by ID, dan JSON by ID.
```python
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
```

`show_xml` / `show_json`

- Ambil semua Player (Player.objects.all()),

- Ubah ke XML/JSON dengan serializers.serialize(...),

- Kembalikan via HttpResponse dengan content_type yang sesuai.

`show_xml_by_id` 

- Pakai filter(pk=player_id) sehingga hasilnya QuerySet (iterable) — itu yang dibutuhkan serializers.serialize('xml', ...).

- Jika tidak ada, return 404.

`show_json_by_id`

- Ambil satu objek dengan get(pk=player_id), lalu dibungkus list [...] karena serialize butuh iterable.

- Jika tidak ada, return 404.

#### Selain itu, saya juga menambahkan 3 fitur untuk pembuatan, lihat detail, dan penghapusan objek  pada views.py
```python
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
```
`register_player`

- Membuat form dari `PlayerForm` 

- Jika POST dan form.is_valid(): simpan objek baru, lalu redirect ke show_main.

- Jika tidak, render halaman form (`register_player.html`) dengan context form.

`show_player`

- Ambil 1 Player berdasarkan pk (id) atau 404 jika tidak ada.

- Render template detail (`player_detail.html`) dengan context player.

`delete_player`
- Ambil Player berdasarkan pk (id) atau 404.

- Hapus objek, tampilkan flash message sukses, lalu redirect ke show_main.
 ### Membuat routing URL untuk masing-masing views yang telah ditambahkan pada poin 1.
 #### Pada `urls.py` tambahkan path(`...`) untuk fungsi-fungsi yang ada di `views.py`
 ```python
 urlpatterns = [
    path('', show_main, name='show_main'),
    path('register-player/', register_player, name='register_player'),
    path('player/<str:id>/', show_player, name='show_player'),
    path('delete-player/<str:id>/', delete_player, name='delete_player'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:player_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:player_id>/', show_json_by_id, name='show_json_by_id'),
]
```

 ### Membuat halaman yang menampilkan data objek model yang memiliki tombol "Add" yang akan redirect ke halaman form, serta tombol "Detail" pada setiap data objek model yang akan menampilkan halaman detail objek.
#### Buat direktori `templates` pada direktori utama lalu buat file `base.html`
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    {% block meta %} {% endblock meta %}
</head>

<body>
    {% block content %} {% endblock content %}
</body>
</html>
```
#### Pada `settings.py` di direktori proyek, tambahkan pada `TEMPLATES`
```python
'DIRS': [BASE_DIR / 'templates']
```
#### Membuat halaman main
```html

<h1>Transfer Market</h1>

<h5>NPM: </h5>
<p>{{ npm }}</p>

<h5>Name:</h5>
<p>{{ name }}</p>

<h5>Class:</h5>
<p>{{ class }}</p>

<a href="{% url 'main:register_player' %}">
  <button>+Register Player</button>
</a>

<hr>

{% if not player_list %}
<p>Belum ada data player pada market.</p>
{% else %}

{% for player in player_list %}
<div>
  <h2><a href="{% url 'main:show_player' player.id %}">{{ player.name }}</a></h2>

  <p><b>{{ player.get_category_display }}</b>{% if player.is_featured %} | 
    <b>Featured</b>{% endif %} 
</p>

  {% if player.thumbnail %}
  <img src="{{ player.thumbnail }}" alt="thumbnail" width="150" height="100">
  <br />
  {% endif %}
    <p>Club: {{ player.club }}</p>
    <p>Price: ${{ player.price }}</p>
    <p>Description: {{ player.description|truncatewords:20 }}...</p>


  <p><a href="{% url 'main:show_player' player.id %}"><button>Detail</button></a></p>
</div>

<hr>
{% endfor %}

{% endif %}

```


 ### Membuat halaman form untuk menambahkan objek model pada app sebelumnya.
 #### Membuat `forms.py` di direktori `main`
 ```python
 from django.forms import ModelForm
from main.models import Player

class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'price', 'description', 'thumbnail', 'category', 'is_featured', 'club', 'nationality', 'height']
 ```
 #### Membuat `register_player.html` di direktori `templates` pada `main`, tampilan ketika menambahkan objek
 ```html
 {% extends 'base.html' %} 
{% block content %}
<h1>Register Player</h1>

<form method="POST">
  {% csrf_token %}
  <table>
    {{ form.as_table }}
    <tr>
      <td></td>
      <td>
        <input type="submit" value="Register Player" />
      </td>
    </tr>
  </table>
</form>

{% endblock %}
 ```
 ### Membuat halaman yang menampilkan detail dari setiap data objek model.

 #### Membuat halaman detail objek, `player_detail.html` pada direktori `templates` di `main` 
```html
{% extends 'base.html' %}
{% block content %}
<p><a href="{% url 'main:show_main' %}"><button>← Back to Player List</button></a></p>

<h1>{{ player.name }}</h1>
<p><b>{{ player.get_category_display }}</b>{% if player.is_featured %} | 
    <b>Featured</b>{% endif %}
</p>

{% if player.thumbnail %}
<img src="{{ player.thumbnail }}" alt="Player thumbnail" width="300">
<br /><br />
{% endif %}
<p>Club: {{ player.club }}</p>
<p>Price: ${{ player.price }}|</p>
<p>Nationality: {{ player.nationality }}</p>
<p>Height: {{ player.height }} cm</p>
<p>{{ player.description }}</p>
<form action="{% url 'main:delete_player' player.id %}" method="post" style="display: inline;">
    {% csrf_token %}
    <button type="submit" onclick="return confirm('Are you sure you want to delete this player?');">Delete Player</button>

{% endblock content %}
```
## Apakah ada feedback untuk asdos di tutorial 2 yang sudah kalian kerjakan?
tidak ada

## Postman
- JSON
https://drive.google.com/file/d/1_ZTEc6esu3nQT3EKey1PT57Lb7mzDU1w/view?usp=sharing
- JSON by ID 
https://drive.google.com/file/d/1yZewIaGM7BHJfhQoqJnKnMWVJriI76MS/view?usp=sharing
- XML 
https://drive.google.com/file/d/16htc-wc_haHn-c4UjztkHyzFHh4ZGddx/view?usp=sharing
- XMl by ID
https://drive.google.com/file/d/1Se_8Oc-SHT9ZwW7p0DxKAyTRo-aGZd-2/view?usp=sharing

</details>