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
Menurut saya, isi dan informasi tutorial 1 sudah lengkap, mudah diikuti dan informatif dengan setiap penjelasannya yang mudah dipahami. Asdos juga sudah selalu bersedia dengan stand by di voice channel server discord jika ada pertanyaan atau error.