<details>
<summary> Tugas 2 </summary>

### Link PWS: https://pbp.cs.ui.ac.id/web/project/daffa.abhinaya/transfermarket

## 1. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step.
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

<details>
<summary> Tugas 4 </summary>

## Apa itu Django AuthenticationForm? Jelaskan juga kelebihan dan kekurangannya.
form built-in Django `django.contrib.auth.forms.AuthenticationForm` yang digunakan untuk login berbasis username + password. Saat divalidasi `is_valid()`, form ini memanggil `authenticate()`; jika berhasil, objek user disimpan dapat diambil via `form.get_user()`, dan jika gagal muncul error “invalid login”. Ia juga punya hook `confirm_login_allowed(user)` yang secara default menolak user yang tidak aktif. Di Tutorial 3 sebelumnya, form ini dipakai dalam view login: saat POST divalidasi, lalu dilakukan `login(request, user)`; saat GET form dirender ke template.

#### Kelebihan:
- Siap pakai dan terintegrasi: langsung bekerja dengan `LoginView`(defaultnya memakai `AuthenticationForm`) dan alur `authenticate()` -> `login()`. 

- Validasi kredensial: seluruh proses authentication dilakukan saat form divalidasi; error ditangani sebagai bagian dari validasi form. 

- Kebijakan login bisa di-custom: override `confirm_login_allowed()` (misalnya, menolak user yang belum verifikasi)

#### Kekurangan:
- Terbatas pada skema username dan password. Untuk kebutuhan lain (email-only login, SSO) perlu kustomisasi form/backends 

- UI dan feedback: perubahan label/pesan/error perlu subclass/override (tidak langsung “plug-and-play” di template). 

- Tidak mencakup fitur proteksi yang lebih advanced seperti rate limiting, CAPTCHA, atau 2FA. (Umumnya ditangani third-party)

## Apa perbedaan antara autentikasi dan otorisasi? Bagaiamana Django mengimplementasikan kedua konsep tersebut?
- Autentikasi = memastikan siapa pengguna (verifikasi kredensial).
- Otorisasi = menentukan apa yang boleh dilakukan pengguna yang sudah terautentikasi

### Implementasi
- Register: tampilkan `UserCreationForm (GET)`, lalu saat `POST → form.is_valid()` → `form.save()` buat akun baru → redirect ke halaman login. 

- Login (autentikasi): gunakan AuthenticationForm; jika valid, ambil user `form.get_user()`, lalu `login(request, user)` untuk membuat session. Setelah itu `request.user.is_authenticated == True` di request berikutnya.  

- Proteksi halaman (otorisasi dasar): batasi akses view dengan `@login_required(...)` agar hanya user terautentikasi yang bisa membuka halaman/fitur tertentu. 

- Kaitkan data dengan user: tambahkan`ForeignKey(User)` pada model (misalnya, `Player.user`) lalu filter query dengan `request.user`, membuat tiap user hanya melihat/mengelola datanya sendiri (pola otorisasi berbasis kepemilikan). 

- Logout: panggil `logout(request)` untuk menghapus session (dan kalau di tutorial sebelumnya, hapus juga cookie `last_login`) lalu redirect.

## Apa saja kelebihan dan kekurangan session dan cookies dalam konteks menyimpan state di aplikasi web?

### Sessions (server-side)

#### Kelebihan

- Lebih aman: data disimpan di server; klien hanya pegang session ID (dalam cookie). Sulit dimodifikasi pengguna.

- Kapasitas lebih bebas: cocok untuk state kompleks (misalnya, keranjang belanja, progress, flash messages).

- Kendali : bisa di-invalidate/expire dari server (misalnya paksa logout).

#### Kekurangan

- Biaya operasional: perlu storage (DB/Redis/memori) dan mekanisme cleanup; menambah lookup per request.

- Skalabilitas: perlu shared store atau sticky session saat multi-server.

### Cookies (client-side)

#### Kelebihan

- Stateless untuk server: tidak perlu penyimpanan di server; mudah diskalakan.

- Persisten: bisa bertahan lama (misalnya, fitur “remember me” dan preferensi UI).

- Sederhana: cukup set key–value; otomatis terkirim ke server pada domain terkait.

#### Kekurangan

- Batas ukuran: kecil (4KB per cookie) dan jumlahnya dibatasi; ikut menambah ukuran setiap request.

- Risiko keamanan: bisa dicuri via XSS jika tidak HttpOnly; bisa disadap jika tidak Secure/HTTPS; bisa dimodifikasi jika tidak ditandatangani/terenkripsi.

- Privasi dan kompatibilitas: bisa diblokir pengguna/aturan browser; perlu sesuai kebijakan privasi.

- Tidak cocok untuk data sensitif/kompleks.

- Keamanan tetap perlu dijaga: jika session ID bocor (tanpa HTTPS/HttpOnly), akun bisa diambil alih; perlu rotasi ID saat login (anti session fixation) dan CSRF token untuk aksi POST.

## Apakah penggunaan cookies aman secara default dalam pengembangan web, atau apakah ada risiko potensial yang harus diwaspadai? Bagaimana Django menangani hal tersebut?
Cookies tidak secara default aman. Browser akan mengirimnya ke server terkait pada tiap request, 
#### Risiko potensial jika tidak dikonfigurasi dengan benar:

- Penyadapan jika tanpa HTTPS → solusinya Secure dan HTTPS.

- Pencurian via XSS (script jahat membaca cookie) → set HttpOnly agar JS tidak bisa mengakses cookie sensitif (misalnya, session).

- CSRF (browser mengirim cookie ke situsmu dari halaman pihak ketiga) → gunakan SameSite (Lax/Strict) dan CSRF token.

- Modifikasi/peniruan nilai oleh klien → jangan simpan data sensitif langsung di cookie

#### Bagaimana Django menanganinya

- Session server-side (default): Django menyimpan state di server; klien hanya memegang session ID di cookie sessionid. Secara default `HttpOnly = True`, sehingga tidak bisa dibaca JS.

- CSRF protection: CsrfViewMiddleware dan token per form; Django memakai CSRF cookie terpisah dan memverifikasi token pada POST.

- SecurityMiddleware membantu HTTPS/HSTS.

- Signed/encrypted cookies: bila memang harus menyimpan data di cookie, Django menyediakan signed cookies `response.set_signed_cookie(...)` dan utilitas `django.core.signing.`

## Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial)

### Mengimplementasikan fungsi registrasi, login, dan logout 
#### Pada `views.py` import 
`UserCreationForm`,`AuthenticationForm`, `messages` `authenticate`, `login`, `logout`.

#### Membuat fungsi register, login, logout di `views.py`
```python
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
            return redirect('main:show_main')

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('main:login')
```
#### Routing URL pada `urls.py` di main
```python
from main.views import register, login_user, logout_user
 urlpatterns = [
     path('register/', register, name='register'),
     path('login/', login_user, name='login'),
     path('logout/', logout_user, name='logout'),
 ]
```
#### Buat halaman html di direktori templates di main
- `register.html`
```html
{% extends 'base.html' %}

{% block meta %}
<title>Register</title>
{% endblock meta %}

{% block content %}

<div>
  <h1>Register</h1>

  <form method="POST">
    {% csrf_token %}
    <table>
      {{ form.as_table }}
      <tr>
        <td></td>
        <td><input type="submit" name="submit" value="Daftar" /></td>
      </tr>
    </table>
  </form>

  {% if messages %}
  <ul>
    {% for message in messages %}
    <li>{{ message }}</li>
    {% endfor %}
  </ul>
  {% endif %}
</div>

{% endblock content %}
```
- `login.html`
```html
{% extends 'base.html' %}

{% block meta %}
<title>Login</title>
{% endblock meta %}

{% block content %}
<div class="login">
  <h1>Login</h1>

  <form method="POST" action="">
    {% csrf_token %}
    <table>
      {{ form.as_table }}
      <tr>
        <td></td>
        <td><input class="btn login_btn" type="submit" value="Login" /></td>
      </tr>
    </table>
  </form>

  {% if messages %}
  <ul>
    {% for message in messages %}
    <li>{{ message }}</li>
    {% endfor %}
  </ul>
  {% endif %} Don't have an account yet?
  <a href="{% url 'main:register' %}">Register Now</a>
</div>

{% endblock content %}
```
#### Menambahkan tombol logout di halaman utama `main.html`
```html
<a href="{% url 'main:logout' %}">
  <button>Logout</button>
</a>
```
#### Restriksi supaya harus registrasi dan login terlebih dahulu untuk masuk ke halaman utama `main`
- Import decorator `login_required` di `views.py`
- Tambahkan `@login_required(login_url='/login')` di atas fungsi `show_main` dan `show_player`

### Membuat dua (2) akun pengguna dengan masing-masing tiga (3) dummy data pada lokal
Registrasi/buat dua akun baru di localhost lalu login salah satu akun dan buat 3 produk. Kemudian ulangi lagi untuk akun satunya.

### Menghubungkan model Product dengan User.
- Import User dari django.contrib.auth.models pada `models.py`
- Tambahkan user di dalam class model product `player`
```python
user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
```
- Lakukan migrasi model

- Ubah code pada fungsi `register_player` di `views.py`
```python
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
```
- Ubah code pada fungsi `show_main`
```python
@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'all':
        player_list = Player.objects.all()
    else:
        player_list = Player.objects.filter(user=request.user)
    context = {
        'npm': '2406405720',  # Ganti dengan NPM kamu
        'name': request.user.username,  # Ganti dengan nama kamu
        'class': 'PBP C',  # Ganti dengan kelas kamu
        'aplikasi': 'Transfer Market',
        'player_list': player_list,
        
    }
    return render(request, 'main.html', context)
```
- Membuat tombol untuk mem-filter product/player pribadi dan All player pada `main.html`
```html
<a href="?filter=all">
  <button type="button">All Players</button>
</a>
<a href="?filter=my">
  <button type="button">My Players</button>
```
- Menambahkan tampilan `user` yang me-register product/player di `player_detail.html`
```html
{% if news.user %}
    <p>Manager: {{ news.user.username }}</p>
{% else %}
    <p>Manager: Anonymous</p>
{% endif %}

```

### Menampilkan detail informasi pengguna yang sedang logged in seperti username dan menerapkan cookies seperti last_login pada halaman utama aplikasi.
- Import `HttpResponseRedirect`, `reverse`, dan `datetime` di `views.py`
- Pada fungsi `login_user` edit bagian `if form.is_valid()`
```python
if form.is_valid():
    user = form.get_user()
    login(request, user)
    response = HttpResponseRedirect(reverse("main:show_main"))
    response.set_cookie('last_login', str(datetime.datetime.now()))
    return response
```
- Tambahkan `last_login` di `context` pada fungsi `show_main`
```python
'last_login': request.COOKIES.get('last_login', 'Never')
```

- Delete cookie `last_login` setelah logout
```python
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response
```
- Menambahkan tampilan informasi waktu terakhir `user` login di `main.html`
```html
<h5>Sesi terakhir login: {{ last_login }}</h5>
```
</details>

<details>
<summary> Tugas 5 </summary>

## Jika terdapat beberapa CSS selector untuk suatu elemen HTML, jelaskan urutan prioritas pengambilan CSS selector tersebut!
- !important paling atas
- Inline style
- stylesheet. 
- Specificity: ID #id 
- class/atribut/pseudo-class .c [attr] :hover 
- elemen/pseudo-elemen h1 ::before. 

Ketika ada 2 selector dengan hierarki sama, selector yang terakhir yang dipakai

## Mengapa responsive design menjadi konsep yang penting dalam pengembangan aplikasi web? Berikan contoh aplikasi yang sudah dan     menerapkan responsive design, serta jelaskan mengapa!
Responsive design penting karena akan lebih nyaman dipakai di berbagai ukuran layar pada web (mobile dan desktop) dengan satu basis kode untuk meningkatkan pengalaman user dan aksesibilitas.
#### Contoh yang sudah responsive design: Wikipedia
 karena arsitekturnya memang memisahkan skin desktop vs mobile. Untuk trafik mobile, Wikimedia memakai skin Minerva Neue yang responsif dan beradaptasi ke perangkat seluler, didorong oleh ekstensi MobileFrontend (Minerva = default untuk proyek Wikimedia di perangkat mobile). Ini membuat halaman konten yang mostly teks–gambar tampil rapi di berbagai lebar layar tanpa web terpisah. 

#### Contoh yang belum responsive design: Google Docs 
belum sepenuhnya responsif di web mobile karena strategi utamanya app-first. Google mengarahkan user smartphone untuk memakai aplikasi Google Docs (Android/iOS) dibanding menggunakan browser mobile; banyak fitur lengkap memang tersedia di aplikasi atau di browser desktop. 

## 3 Jelaskan perbedaan antara margin, border, dan padding, serta cara untuk mengimplementasikan ketiga hal tersebut!
- Padding: ruang di dalam kotak, antara konten dan border.
- Border: garis pembatas mengitari padding/konten.
- Margin: ruang di luar border, memisahkan elemen dari elemen lain.
Box model diatur oleh properti ini; `box-sizing: border-box`; membuat width/height sudah termasuk padding+border 

Contoh: 
```css
.card {
  margin: 16px;            /* luar */
  border: 1px solid #ddd;  /* garis tepi */
  padding: 12px;           /* dalam */
  box-sizing: border-box;
}
```

## Jelaskan konsep flex box dan grid layout beserta kegunaannya!
- Flexbox, layout satu dimensi (hanya bisa baris atau kolom). Biasanya cocok untuk navbar, dan kumpulan tombol. Contoh:
```css
.row { display: flex; gap: 12px; align-items: center; justify-content: space-between; }
```
- Grid, layout dua dimensi (bisa baris dan kolom) Biasanya cocok untuk layout halaman dan dashboard. Contoh:
```css
.grid { display: grid; grid-template-columns: 1fr 2fr; gap: 16px; }
```

## Implementasi checklist secara step-by-step
### Fungsi untuk menghapus dan mengedit product.
Membuat fungsi `delete_player` dan `edit_player` pada `views.py`
```python
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
```
Routing `urls.py`
pada `urls.py` import `delete_player` dan `edit_player` dan tambahkan
```python
path('delete-player/<str:id>/', delete_player, name='delete_player'),
path('edit/<uuid:id>/edit', edit_player, name='edit_player'),
```

### Kustomisasi halaman login, register, tambah product, edit product, dan detail product semenarik mungkin.
- Menambahkan styling Tailwind dan `global.css`. Buat file `global.css` pada `css` dengan buat folder baru `static/css` pada `transfer-market`
```css
.form-style form input, form textarea, form select {
    width: 100%;
    padding: 0.5rem;
    border: 2px solid #bcbcbc;
    border-radius: 0.375rem;
}
.form-style form input:focus, form textarea:focus, form select:focus {
    outline: none;
    border-color: #16a34a;
    box-shadow: 0 0 0 3px #16a34a;
}

.form-style input[type="checkbox"] {
    width: 1.25rem;
    height: 1.25rem;
    padding: 0;
    border: 2px solid #d1d5db;
    border-radius: 0.375rem;
    background-color: white;
    cursor: pointer;
    position: relative;
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
}

.form-style input[type="checkbox"]:checked {
    background-color: #16a34a;
    border-color: #16a34a;
}

.form-style input[type="checkbox"]:checked::after {
    content: '✓';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-weight: bold;
    font-size: 0.875rem;
}

.form-style input[type="checkbox"]:focus {
    outline: none;
    border-color: #16a34a;
    box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1);
}

```
Edit file `base.html`
```html
{% load static %}

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    {% block meta %} {% endblock meta %}
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="{% static 'css/global.css' %}"/>
  </head>
  <body>
    {% block content %} {% endblock content %}
  </body>
</html>
```
- Edit `login.html` untuk kustomisasi halaman login
```html
{% extends 'base.html' %}
{% block meta %}
<title>Login - Transfer Market</title>
{% endblock meta %}

{% block content %}
<div class="bg-gray-100 min-h-screen flex items-center justify-center py-8 px-4">
  <div class="max-w-md w-full">
    <div class="bg-white border border-gray-200 rounded-md p-6 form-style">
      <h1 class="text-xl font-semibold mb-4">Sign In</h1>

      {% if form.non_field_errors %}
        <div class="mb-4 text-sm text-red-700 bg-red-50 border border-red-200 rounded p-3">
          {% for error in form.non_field_errors %}{{ error }}{% endfor %}
        </div>
      {% endif %}
      {% if form.errors %}
        <div class="mb-4 text-sm text-red-700 bg-red-50 border border-red-200 rounded p-3">
          {% for field, errors in form.errors.items %}
            {% if field != '__all__' %}
              {% for error in errors %}<div>{{ field|title }}: {{ error }}</div>{% endfor %}
            {% endif %}
          {% endfor %}
        </div>
      {% endif %}

      <form method="POST" action="" class="space-y-4">
        {% csrf_token %}
        <div>
          <label for="username" class="block text-sm font-medium text-gray-800 mb-1">Username</label>
          <input id="username" name="username" type="text" required class="w-full px-3 py-2 border border-gray-300 rounded"/>
        </div>
        <div>
          <label for="password" class="block text-sm font-medium text-gray-800 mb-1">Password</label>
          <input id="password" name="password" type="password" required class="w-full px-3 py-2 border border-gray-300 rounded"/>
        </div>
        <button type="submit" class="w-full bg-green-600 text-white px-4 py-2 rounded">Sign In</button>
      </form>

      <div class="mt-6 text-center border-t border-gray-200 pt-4 text-sm">
        <span class="text-gray-600">Don't have an account?</span>
        <a href="{% url 'main:register' %}" class="text-green-700"> Register</a>
      </div>
    </div>
  </div>
</div>
{% endblock content %}
```
- Kustomisasi `register.html`
```html
{% extends 'base.html' %}
{% block meta %}
<title>Register - Transfer Market</title>
{% endblock meta %}

{% block content %}
<div class="bg-gray-100 min-h-screen flex items-center justify-center py-8 px-4">
  <div class="max-w-md w-full">
    <div class="bg-white border border-gray-200 rounded-md p-6 form-style">
      <h1 class="text-xl font-semibold mb-4">Create Account</h1>

      {% if form.non_field_errors %}
        <div class="mb-4 text-sm text-red-700 bg-red-50 border border-red-200 rounded p-3">
          {% for error in form.non_field_errors %}{{ error }}{% endfor %}
        </div>
      {% endif %}
      {% if form.errors %}
        <div class="mb-4 text-sm text-red-700 bg-red-50 border border-red-200 rounded p-3">
          {% for field, errors in form.errors.items %}
            {% if field != '__all__' %}
              {% for error in errors %}<div>{{ field|title }}: {{ error }}</div>{% endfor %}
            {% endif %}
          {% endfor %}
        </div>
      {% endif %}

      <form method="POST" action="" class="space-y-4">
        {% csrf_token %}
        <div>
          <label for="username" class="block text-sm font-medium text-gray-800 mb-1">Username</label>
          <input id="username" name="username" type="text" required class="w-full px-3 py-2 border border-gray-300 rounded"/>
        </div>
        <div>
          <label for="password1" class="block text-sm font-medium text-gray-800 mb-1">Password</label>
          <input id="password1" name="password1" type="password" required class="w-full px-3 py-2 border border-gray-300 rounded"/>
        </div>
        <div>
          <label for="password2" class="block text-sm font-medium text-gray-800 mb-1">Confirm Password</label>
          <input id="password2" name="password2" type="password" required class="w-full px-3 py-2 border border-gray-300 rounded"/>
        </div>
        <button type="submit" class="w-full bg-green-600 text-white px-4 py-2 rounded">Create Account</button>
      </form>

      <div class="mt-6 text-center text-sm">
        <a href="{% url 'main:login' %}" class="text-green-700">Already have an account? Sign in</a>
      </div>
    </div>
  </div>
</div>
{% endblock content %}
```
- Kustomisasi `register_player.html` untuk tambah product
```html
{% extends 'base.html' %}
{% block meta %}
<title>Register Player - Transfer Market</title>
{% endblock meta %}
{% block content %}
<div class="bg-gray-100 min-h-screen py-8">
  <div class="max-w-3xl mx-auto px-4">

    <a href="{% url 'main:show_main' %}" class="text-sm text-gray-700">← Back</a>

    <div class="bg-white border border-gray-200 rounded-md mt-4">
      <div class="px-6 py-4 border-b border-gray-200">
        <h1 class="text-xl font-semibold">Register Player</h1>
        <p class="text-gray-600 text-sm">Add a new football player to the market.</p>
      </div>

      <div class="px-6 py-5 form-style">
        <form method="POST" class="space-y-4">
          {% csrf_token %}
          {% for field in form %}
            <div>
              <label for="{{ field.id_for_label }}" class="block text-sm font-medium text-gray-800 mb-1">{{ field.label }}</label>
              {{ field }}
              {% if field.help_text %}
                <p class="text-xs text-gray-500 mt-1">{{ field.help_text }}</p>
              {% endif %}
              {% for error in field.errors %}
                <p class="text-xs text-red-600 mt-1">{{ error }}</p>
              {% endfor %}
            </div>
          {% endfor %}

          <div class="pt-4 flex items-center gap-3">
            <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded">Submit</button>
            <a href="{% url 'main:show_main' %}" class="px-4 py-2 border border-gray-300 rounded text-gray-800">Cancel</a>
          </div>
        </form>
      </div>
    </div>

  </div>
</div>
{% endblock %}
```
- Kustomisasi `edit_player.html` untuk edit product
```html
{% extends 'base.html' %}
{% block meta %}
<title>Edit Player - Transfer Market</title>
{% endblock meta %}

{% block content %}
<div class="bg-gray-100 min-h-screen py-8">
  <div class="max-w-3xl mx-auto px-4">

    <a href="{% url 'main:show_main' %}" class="text-sm text-gray-700">← Back</a>

    <div class="bg-white border border-gray-200 rounded-md mt-4">
      <div class="px-6 py-4 border-b border-gray-200">
        <h1 class="text-xl font-semibold">Edit Player</h1>
        <p class="text-gray-600 text-sm">Update player information.</p>
      </div>
      <div class="px-6 py-5 form-style">
        <form method="POST" class="space-y-4">
          {% csrf_token %}
          {% for field in form %}
            <div>
              <label for="{{ field.id_for_label }}" class="block text-sm font-medium text-gray-800 mb-1">{{ field.label }}</label>
              {{ field }}
              {% for error in field.errors %}
                <p class="text-xs text-red-600 mt-1">{{ error }}</p>
              {% endfor %}
            </div>
          {% endfor %}
          <div class="pt-4 flex items-center gap-3">
            <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded">Save</button>
            <a href="{% url 'main:show_main' %}" class="px-4 py-2 border border-gray-300 rounded text-gray-800">Cancel</a>
          </div>
        </form>
      </div>
    </div>

  </div>
</div>
{% endblock %}
```
- Kustomisasi `player_detail.html` untuk detail product
```html
{% extends 'base.html' %}

{% block meta %}
<title>{{ player.name }} - Transfer Market</title>
{% endblock meta %}

{% block content %}
<div class="bg-gray-100 min-h-screen py-8">
  <div class="max-w-6xl mx-auto px-4">

    <a href="{% url 'main:show_main' %}" class="text-sm text-gray-700">← Back to list</a>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-4">
      <!-- Left: Photo & basic info -->
      <div class="bg-white border border-gray-200 rounded-md p-4">
        {% if player.thumbnail %}
          <img src="{{ player.thumbnail }}" alt="{{ player.name }}" class="w-full h-64 object-cover rounded"/>
        {% else %}
          <div class="w-full h-64 bg-gray-200 rounded"></div>
        {% endif %}
        <div class="mt-4">
          <div class="text-lg font-semibold">{{ player.name }}</div>
          <div class="text-sm text-gray-600">{{ player.club }}</div>
          <div class="text-sm text-gray-600">{{ player.nationality }}</div>
        </div>
      </div>

      <!-- Right: Details -->
      <div class="lg:col-span-2 bg-white border border-gray-200 rounded-md">
        <div class="px-6 py-4 border-b border-gray-200">
          <h1 class="text-xl font-semibold">Player Profile</h1>
        </div>
        <div class="px-6 py-5">
          <dl class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-4 text-sm">
            <div>
              <dt class="text-gray-600">Position</dt>
              <dd class="font-medium">{{ player.get_category_display|default:player.category }}</dd>
            </div>
            <div>
              <dt class="text-gray-600">Height</dt>
              <dd class="font-medium">{{ player.height }} cm</dd>
            </div>
            <div>
              <dt class="text-gray-600">Price</dt>
              <dd class="font-medium">Rp {{ player.price }}</dd>
            </div>
          </dl>
          {% if player.description %}
            <div class="mt-6">
              <div class="text-gray-800 text-sm leading-relaxed whitespace-pre-line">{{ player.description }}</div>
            </div>
          {% endif %}
        </div>
        <div class="px-6 py-4 border-t border-gray-200 flex items-center justify-between">
          <div class="flex items-center gap-3">
            {% if user.is_authenticated and player.user == user %}
              <a href="{% url 'main:edit_player' player.id %}" class="px-3 py-2 border border-gray-300 rounded text-gray-800 text-sm">Edit</a>
              <form action="{% url 'main:delete_player' player.id %}" method="post">
                {% csrf_token %}
                <button type="submit" class="px-3 py-2 bg-red-600 text-white rounded text-sm">Delete</button>
              </form>
            {% endif %}
          </div>
        </div>
      </div>
    </div>

  </div>
</div>
{% endblock content %}
```

### Kustomisasi halaman daftar product menjadi lebih menarik dan responsive. 
- Kustomisasi `main.html` 
```html
{% extends 'base.html' %}
{% load static %}

{% block meta %}
<title>Transfer Market</title>
{% endblock meta %}

{% block content %}
{% include 'navbar.html' %}

<div class="bg-gray-100 min-h-screen pt-16 py-8">
  <div class="max-w-7xl mx-auto px-4">

    <div class="mb-4 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold">Players Market</h1>
        <p class="text-sm text-gray-600">Browse football players and their market details.</p>
      </div>
      <a href="{% url 'main:register_player' %}" class="bg-green-600 text-white px-4 py-2 rounded">
        Register Player
      </a>
    </div>

    {# Tabs: All / My #}
    <div class="mb-4 bg-white border border-gray-200 rounded-md p-3">
      <div class="flex items-center gap-2 text-sm">
        <a href="?" class="px-3 py-1 rounded {% if request.GET.filter == 'all' or not request.GET.filter %} bg-green-600 text-white {% else %} border border-gray-300 text-gray-800 {% endif %}">All Players</a>
        <a href="?filter=my" class="px-3 py-1 rounded {% if request.GET.filter == 'my' %} bg-green-600 text-white {% else %} border border-gray-300 text-gray-800 {% endif %}">My Players</a>
        {% if user.is_authenticated and last_login %}
          <span class="ml-auto text-gray-500">Last login: {{ last_login }}</span>
        {% endif %}
      </div>
    </div>

    {% if player_list %}
      {# Deretan kartu horizontal (satu kartu per pemain) #}
      <div class="space-y-3">
        {% for p in player_list %}
          {% include 'card_player.html' with player=p %}
        {% endfor %}
      </div>
    {% else %}
      <div class="bg-white border border-gray-200 rounded-md p-12 text-center">
        <div class="w-24 h-24 mx-auto mb-3">
          <img src="{% static 'image/no-player.png' %}" class="w-full h-full object-contain" alt="No players"/>
        </div>
        <p class="text-gray-700 mb-4">No players found.</p>
        <a href="{% url 'main:register_player' %}" class="bg-green-600 text-white px-4 py-2 rounded">Register Player</a>
      </div>
    {% endif %}

  </div>
</div>
{% endblock content %}

```

### Untuk setiap card product, buatlah dua buah button untuk mengedit dan menghapus product pada card tersebut!
- Edit `card_player.html` ketika ingin edit/delete `product` tanpa melihat detail, bisa dengan pencet tombol titik tiga lalu pilih edit/delete
```html
<article class="bg-white border border-gray-200 rounded-md p-3">
<div class="flex items-center gap-3">
    {% if player.thumbnail %}
    <a href="{% url 'main:show_player' player.id %}">
        <img src="{{ player.thumbnail }}" alt="{{ player.name }}" class="w-14 h-14 object-cover rounded">
    </a>
    {% else %}
    <div class="w-14 h-14 bg-gray-200 rounded"> </div>
    {% endif %}

    <div class="flex-1 min-w-0">
        <div class="flex items-center gap-2">
            <a href="{% url 'main:show_player' player.id %}" class="font-semibold text-gray-900 truncate">{{ player.name }}</a>
            {% if player.is_featured %}
                <span class="inline-block text-[10px] px-2 py-0.5 bg-yellow-100 text-yellow-800 border border-yellow-200 rounded">Featured</span>
            {% endif %}
        </div>

            <div class="mt-1 flex flex-wrap gap-1">
            <span class="inline-block text-[10px] px-2 py-0.5 bg-blue-100 text-blue-800 border border-blue-200 rounded">{{ player.get_category_display|default:player.category }}</span>
            <span class="inline-block text-[10px] px-2 py-0.5 bg-green-100 text-green-800 border border-green-200 rounded">{{ player.club }}</span>
            <span class="inline-block text-[10px] px-2 py-0.5 bg-gray-100 text-gray-800 border border-gray-200 rounded">{{ player.nationality }}</span>
            </div>

    </div>


    <div class="text-right">
        {% if user.is_authenticated and player.user_id == user.id %}
        <details class="relative inline-block">
        <summary class="list-none px-2 py-1 border border-gray-300 rounded text-gray-800 cursor-pointer" aria-label="Actions">⋯</summary>
        
        <div class="absolute right-0 mt-1 w-36 bg-white border border-gray-200 rounded z-10">
        <a href="{% url 'main:edit_player' player.id %}" class="block px-3 py-2 text-sm text-gray-800">Edit</a>
        <a href="{% url 'main:delete_player' player.id %}" class="block px-3 py-2 text-sm text-red-700">Delete</a>

        </div>
        </details>
        {% endif %} 
    </div>

</div>
</article>
```
### Buatlah navigation bar (navbar) untuk fitur-fitur pada aplikasi yang responsive terhadap perbedaan ukuran device, khususnya mobile dan desktop.
Buat file `navbar.html` pada `templates` di root
```html
<nav class="fixed top-0 left-0 w-full bg-white border-b border-gray-200 z-50">
  <div class="max-w-7xl mx-auto px-6 lg:px-8">
    <div class="flex items-center justify-between h-16">
      <div class="text-xl font-semibold text-gray-900"><span class="text-green-600">Transfer</span> Market</div>
      <div class="hidden md:flex items-center gap-6">
        <a href="/" class="text-gray-700">Home</a>
        <a href="{% url 'main:register_player' %}" class="text-gray-700">Register Player</a>
      </div>
      <div class="hidden md:flex items-center gap-4">
        {% if user.is_authenticated %}
          <div class="text-right text-sm">
            <div class="font-medium text-gray-900">{{ name|default:user.username }}</div>
            <div class="text-gray-500">{{ npm|default:"Student" }} - {{ class|default:"Class" }}</div>
          </div>
          <a href="{% url 'main:logout' %}" class="text-red-700">Logout</a>
        {% else %}
          <a href="{% url 'main:login' %}" class="text-gray-700">Login</a>
          <a href="{% url 'main:register' %}" class="bg-green-600 text-white px-4 py-2 rounded">Register</a>
        {% endif %}
      </div>
      <!-- Simple mobile: always visible links below -->
    </div>
  </div>
  <div class="md:hidden border-t border-gray-200">
    <div class="px-6 py-3 flex items-center gap-4 text-sm">
      <a href="/" class="text-gray-700">Home</a>
      <a href="{% url 'main:register_player' %}" class="text-gray-700">Register Player</a>
      {% if user.is_authenticated %}
        <a href="{% url 'main:logout' %}" class="text-red-700 ml-auto">Logout</a>
      {% else %}
        <a href="{% url 'main:login' %}" class="text-gray-700 ml-auto">Login</a>
        <a href="{% url 'main:register' %}" class="bg-green-600 text-white px-3 py-1 rounded">Register</a>
      {% endif %}
    </div>
  </div>
</nav>
```
</details>


<details>
<summary> Tugas 6 </summary>

##  Perbedaan synchronous request dan asynchronous request
 Synchronous request membuat browser menunggu sampai respons selesai sebelum bisa lanjut menjalankan hal lain. Efeknya interface nampak nge-"freeze" karena satu cycle kerja harus selesai dulu. Sedangkan, Asynchronous reqgituest tidak memblokir eksekusi, halaman tetap responsif sambil menunggu respons, dan ketika data datang barulah bagian tertentu pada halaman diperbarui. Konsep dari AJAX ini memungkinkan untuk update isi halaman tanpa harus reload. 

- Synchronous: blocking, terdapat potensi UI tidak merespons.
- Asynchronous: non-blocking, update bagian halaman saja.

## Alur kerja AJAX di Django
Misal ada event di halaman (misalnya klik tombol atau saat halaman dibuka), JavaScript memanggil fetch ke endpoint Django, server memproses dan mengembalikan JSON, lalu JavaScript membaca respons dan merender ulang elemen DOM yang relevan tanpa reload halaman. Alurnya:
-  event → fetch → view Django → JsonResponse → update DOM. 

Pada sisi server, view Django mengumpulkan data model, mengubahnya menjadi list of dict, lalu mengirimnya sebagai JsonResponse. Pada sisi klien, template menyiapkan kontainer seperti loading, error, grid, dan JavaScript menampilkan atau meng-hide sambil merender `card` untuk `product`

• JsonResponse adalah subclass HttpResponse yang otomatis memberi Content-Type application/json dan mempermudah serialisasi. 

## Keuntungan AJAX dibanding render biasa di Django
User lebih nyaman  karena tidak perlu manual full page reload. Data bisa dipanggil di "belakang" lalu hanya bagian yang perlu diperbarui yang diganti. Jadi, ketika memakai AJAX, JavaScript di halaman mengirim request ke server secara asynchronous lewat fetch atau XMLHttpRequest. Proses jaringan itu ditangani browser di “belakang layar” sehingga halaman tidak melakukan reload penuh dan user masih bisa menekan tombol lain. Setelah respons datang, JavaScript mengambil data yang dibutuhkan lalu memperbarui hanya elemen DOM yang relevan.Bandwidth serta beban render ulang halaman penuh juga berkurang. Contoh

- Responsif dan hemat waktu: hanya bagian yang berubah yang di-update.
- State UI yang jelas: loading spinner, error, empty state, dan notifikasi toast.

## Cara memastikan keamanan saat menggunakan AJAX untuk fitur Login dan Register di Django?


- CSRF protection. Untuk request POST dari AJAX di origin yang sama, sertakan CSRF token ke header atau body. Jangan menonaktifkan CSRF untuk endpoint login atau register. Gunakan `{% csrf_token %}` pada form serta read token di JavaScript ketika melakukan fetch. 

- Validasi sisi server dan proses aman. Gunakan mekanisme Django auth seperti `authenticate` dan form bawaan Django sehingga kredensial diproses oleh komponen yang sudah teruji, bukan oleh logika custom yang raw. 

- Lindungi dari XSS. Membersihkan input di server (misalnya `strip_tags` dalam form clean) dan membersihkan output di client menggunakan DOMPurify sebelum memasukkan string ke innerHTML. Ini mencegah script injection melalui data yang ditampilkan kembali. 

- Pakai HTTPS untuk mengirim kredensial agar terenkripsi saat transit.


## Dampak AJAX terhadap User Experience
AJAX membuat interaksi terasa mulus karena usder tidak dipindah-pindah halaman. Misalnya, saat data dimuat ditampilkan spinner, jika sukses grid konten muncul, jika gagal ada error message, dan untuk aksi seperti membuat data, muncul notifikasi toast. Mekanisme ini meningkatkan rasa kontrol user dan mengurangi friction. 
- Navigasi cepat karena partial update.
- Respon real-time melalui loading state dan toast membantu user memahami apa yang sedang terjadi.

</details>