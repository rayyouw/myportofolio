# Portfolio Website - Rayhan Fairuz Aqram

**Nama** : Rayhan Fairuz Aqram <br>
**NPM** : 2506586186 <br>
**Kelas** : PBP D <br>
**Hobi** : Olahraga <br>
**Tautan PWS** : [https://rayhan-fairuz51-myportofolio.pws.cs.ui.ac.id/](https://rayhan-fairuz51-myportofolio.pws.cs.ui.ac.id/) <br>
**Tautan GitHub** : [https://github.com/rayyouw/myportofolio](https://github.com/rayyouw/myportofolio)

---

# 1. Documentation

### Deskripsi Proyek
Proyek ini adalah website portofolio pribadi berbasis Django yang dikembangkan secara bertahap pada mata kuliah Pemrograman Berbasis Platform (CSGE602022), Fakultas Ilmu Komputer, Universitas Indonesia. Website ini memuat informasi profil, latar belakang pendidikan, riwayat pengalaman profesional & organisasi, pencapaian kompetisi (*awards*), proyek teknologi, serta daftar keahlian (*skills*).

---

### Panduan Setup & Menjalankan Proyek Secara Lokal

1. **Clone Repositori**:
   ```bash
   git clone https://github.com/rayyouw/myportofolio.git
   cd myportofolio
   ```

2. **Buat dan Aktifkan Virtual Environment (Disarankan)**:
   ```bash
   python -m venv env
   # Windows:
   env\Scripts\activate
   # Linux/macOS:
   source env/bin/activate
   ```

3. **Install Dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan Migrasi Database**:
   ```bash
   python manage.py migrate
   ```

5. **Buat Akun Superuser (Pemilik Portofolio)**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Konfigurasi Role Editor**:
   - Jalankan server: `python manage.py runserver`
   - Buka Django Admin di `http://127.0.0.1:8000/admin/`.
   - Buka menu **Groups** $\rightarrow$ Tambah group dengan nama persis: `Editor`.
   - Buka menu **Users** $\rightarrow$ Pilih akun yang ingin dijadikan Editor, lalu centang group `Editor` pada bagian *Permissions/Groups*.

7. **Jalankan Unit Test**:
   ```bash
   python manage.py test
   ```

8. **Akses Website**:
   Buka browser di `http://127.0.0.1:8000/`.

---

### Perkembangan Mingguan (Weekly Progress)

#### **Tugas 1: Static Web dengan HTML5 dan CSS3**
- Membangun halaman *"About Me"* statis menggunakan elemen semantik HTML5 (`<header>`, `<nav>`, `<section>`, `<article>`, `<footer>`).
- Mengimplementasikan layout responsif (desktop & mobile) menggunakan CSS Grid dan Flexbox.
- Menyusun styling kustom di `style.css` untuk bagian profil, pendidikan, pengalaman, penghargaan, dan keahlian.

#### **Tugas 2: Implementasi Model-View-Template (MVT)**
- Menerapkan arsitektur MVT bawaan Django untuk memisahkan data, logika tampilan, dan presentasi.
- Menambahkan model dinamis, membuat migrasi skema database, dan me-render data menggunakan Django Template Language (`{% for %}` dengan fallback `{% empty %}`).
- Menyediakan routing terpisah di `main/urls.py` dan navigasi konsisten di navbar.
- Menambahkan automated test untuk verifikasi routing, template, dan kelengkapan data.

#### **Tugas 3: Form & Data Delivery (JSON)**
- Menerapkan modularisasi template menggunakan inheritance (`base.html`).
- Mengimplementasikan `ModelForm` dengan perlindungan `{% csrf_token %}` untuk operasi pembuatan (*create*), pembaruan (*update*), dan penghapusan (*delete*) data.
- Menyediakan endpoint JSON publik (`/api/projects/`, `/api/awards/`, dll.) melalui serialisasi data Django ORM.

#### **Tugas 4: Authentication, Session, Cookies, & Role-Based Access Control (RBAC)**
- **Autentikasi & Sesi**: Mengimplementasikan registrasi, login, logout berbasis session Django, dan pelacakan aktivitas melalui cookie `last_login`.
- **Role-Based Access Control (4 Tingkat Peran)**:
  1. **Pengunjung (Belum Login)**: Hak akses hanya-baca (*read-only*). Tombol manipulasi data disembunyikan; aksi mutasi & klik bintang dialihkan ke `/login/`.
  2. **Regular User**: Dapat membaca data dan memberi/mencabut bintang (**Star / Unstar**). Upaya manipulasi data ditolak di sisi server dengan HTTP `403 Forbidden` (`PermissionDenied`).
  3. **Editor (Group `Editor`)**: Memiliki hak regular user ditambah hak mengedit/memperbarui data proyek dan *awards*. Tombol `Edit` ditampilkan secara kondisional via `{% if user.is_superuser or is_editor %}`. Tidak memiliki izin menambah baru atau menghapus data.
  4. **Superuser (Pemilik)**: Memiliki hak akses penuh (*CRUD*) terhadap data portofolio dan bintang.
- **Fitur Interaktif Star**: Relasi `ManyToManyField` `starred_by` pada model `Project` untuk mekanisme satu bintang per pengguna, dilengkapi endpoint `toggle_star` dengan verifikasi CSRF.
- **Keamanan Data & Integritas API**: Endpoint `/api/projects/` menyajikan data proyek dan agregat `star_count` tanpa membocorkan identitas pengguna yang membintangi proyek.

---

# 2. Reflective Questions

### Tugas 1
 
**1. Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti `<section>`, `<article>`, atau `<aside>`? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?**
 
Jawab: Ya saya menggunakan beberapa elemen semantik HTML5, seperti `<header>`, `<nav>`, `<section>`, `<article>`, dan `<footer>`, tetapi tidak menggunakan `<aside>` karena saya tidak menggunakan sidebar. Saya menggunakan `<header>` untuk bagian navbar (username, menu navigasi, dan toggle dark/light), `<nav>` untuk link-link di menu navigasi (Profile, Education, Experience, Awards, dan Skills) di dalam `<header>`, `<section>` untuk pembatas tiap-tiap bagian utama (hero/profile, education, experience, awards, dan skills), `<article>` untuk satu entri konten di dalam setiap section, misalnya satu entri experience atau satu entri awards, serta saya menggunakan `<footer>` sebagai bagian penutup halaman berisi copyright. Elemen-elemen ini mempermudah struktur kode sehingga lebih mudah dibaca dibandingkan hanya menggunakan `<div>` generik.
 
**2. Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?**
 
Jawab: Tantangan utama ada di section yang pakai CSS Grid dua kolom (foto + teks), seperti di bagian hero/profile. Di layar sempit, saya ubah `grid-template-areas` jadi susunan vertikal supaya foto tetap besar dan teks tidak terlalu sempit. Untuk grid di section education, experience, awards, dan skills, saya turunkan dari multi-kolom ke 1 kolom penuh di mobile karena keterbacaan teks lebih saya prioritaskan dibanding efisiensi ruang.
 
**3. Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?**
 
Jawab: Ada beberapa batasan yang saya rasakan. Pertama, section experience dan skills yang awalnya ingin difilter (misalkan: experience dibagi lagi menjadi work dan organisasi/kepanitiaan) menggunakan fungsi `:has()` di CSS tidak didukung semua browser. Kedua, preferensi dark/light mode juga tidak bisa disimpan lintas sesi tanpa `localStorage`. Ketiga, form kontak email masih sebatas link `mailto:` tanpa bisa mengirim langsung. Kedepannya, saya ingin mengatasi batasan-batasan tersebut menggunakan JavaScript dan Backend Tools lainnya supaya website lebih fungsional dan dinamis.

### Tugas 2
**1. Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran `urls.py` proyek, `urls.py` aplikasi, view, model, dan template.**
 
Jawab: Request `/projects/` diterima `urls.py` proyek, diteruskan ke `main/urls.py` lewat `include()`, lalu memanggil view `show_projects`. View mengambil data via model (`Project.objects.all()`), memasukkannya ke `context`, dan me-render `projects.html`. Template menampilkan data dengan `{% for %}` (fallback `{% empty %}` jika kosong), lalu hasil HTML dikirim ke browser.
 
**2. Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.**
 
Jawab: Sesuai prinsip MVT, data disimpan di model supaya bisa diubah lewat Django admin tanpa mengedit HTML, dan bisa dipakai ulang di beberapa halaman tanpa duplikasi. Penggunaan model juga mempermudah fitur lanjutan seperti urutan waktu, pilihan tipe, dan lainnya tanpa perlu mengubah template setiap kali ada perubahan data. Hal ini memudahkan maintenance dan pengembangan aplikasi ke depannya.
 
**3. Apa perbedaan fungsi `makemigrations` dan `migrate` pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.**
 
Jawab: `makemigrations` membuat file migrasi berdasarkan perubahan pada model, tanpa mengubah database. `migrate` mengeksekusi file migrasi tersebut ke database sehingga skemanya benar-benar berubah. Contoh nyata di project saya: saat model `Award` ditambahkan ke `models.py`, `python manage.py makemigrations` menghasilkan file `main/migrations/0004_award.py` yang mendeskripsikan tabel baru tersebut, namun database belum berubah sampai `python manage.py migrate` dijalankan untuk benar-benar membuat tabel `Award` di database.

### Tugas 3
**1. Jelaskan mengapa kita menggunakan ModelForm pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan `{% csrf_token %}` pada form tersebut!**

Jawab: Framework Django menyajikan alur kode yang lebih sistematis dan terstruktur, terutama mengenai pengelolaan database setiap kita ingin menambahkan atau mengurangi data tertentu. Jika menggunakan form HTML secara manual, saya harus menulis baris kode HTML satu per satu dan mengedit database secara manual. Kemudian, fungsi `{% csrf_token %}` sendiri bertugas untuk melindungi situs dari serangan CSRF (Cross-Site Request Forgery), yakni serangan yang dilakukan pihak ketiga yang ingin melakukan fraud ke situs tanpa sepengetahuan pengguna yang sedang login.

**2. Pada Tutorial 03, kita membahas format data `JSON` dan `XML`. Mengapa `JSON` lebih disukai dalam pengembangan aplikasi web modern dibandingkan `XML`?**

Jawab: `JSON` memiliki syntax yang lebih mudah dipahami dan ukuran berkas yang lebih ringan dibandingkan `XML`. Selain itu, format `JSON` juga lebih cepat diproses karena strukturnya terintegrasi secara native dengan `JavaScript`.

**3. Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk `JSON`. Mengapa kita perlu melakukan proses serialization pada model `Django` sebelum datanya dikembalikan?**

Jawab: Saat URL diakses, fungsi view Django akan dipicu untuk mengambil data portofolio dari database menggunakan Object-Relational Mapping (ORM). Data tersebut kemudian harus melalui `serialization` untuk diubah dari objek Python (QuerySet) yang kompleks menjadi format data universal seperti dictionary atau teks string. `Serialization` dilakukan karena pada dasarnya situs tidak memahami objek internal `Django` sehingga data perlu diterjemahkan ke format yang netral. Terakhir, view membungkus data hasil serialisasi tersebut ke dalam `JsonResponse` untuk dikirimkan kembali ke klien melalui protokol HTTP.

### Tugas 4
*(Catatan: Pertanyaan refleksi ditiadakan pada Tugas 4 sesuai instruksi tugas)*

---

# 3. AI Disclosure

### Tugas 1
Saya menggunakan **Claude (Anthropic)** sebagai bantuan selama mengerjakan tugas ini, dengan rincian sebagai berikut:
 
**Bagian yang dibantu AI:**
1. Debugging CSS specificity conflict pada fitur filter Experience (rule `.experience-item { display: flex }` menimpa `.timeline-item { display: none }`).
2. Perbaikan bug `scroll-margin-top` supaya judul section tidak tertutup navbar `fixed` saat diklik dari navigasi.
3. Review kode untuk mendeteksi CSS yang redundan/konflik (misalnya dua deklarasi `.hero` yang saling menimpa).
4. Penyusunan pesan commit mengikuti format Conventional Commits.

**Strategi prompting:** Saya memberikan potongan kode HTML/CSS asli saya secara langsung, lalu meminta AI menjelaskan penyebab bug secara spesifik dan optimasi yang bisa dilakukan. 
**Keterbatasan AI yang saya temukan:** Beberapa saran AI kurang match dengan ekspektasi yang saya mau, seperti misalkan membuat foto dan teks sejajar atau mengubah theme color sesuai selera saya. Jadi, saya mengambil kesimpulan bahwa AI belum bisa untuk mengerti secara kompleks kreativitas dari manusia.

### Tugas 2
Saya menggunakan **GitHub Copilot** sebagai bantuan selama mengerjakan tugas ini, dengan rincian sebagai berikut:
 
**Bagian yang dibantu AI:**
1. Bertanya lebih spesifik mengenai alur kerja MVT (Model-View-Template), khususnya bagaimana request mengalir dari `urls.py` proyek hingga sampai ke template.
2. Menambahkan halaman baru yang bersifat looping (menampilkan data lewat `{% for %}`), dengan pola yang sama seperti halaman sebelumnya, tinggal disesuaikan model dan template-nya.
3. Debugging error PostgreSQL yang muncul saat menjalankan migrasi/koneksi database.

**Strategi prompting:** Saya bertanya secara spesifik terkait konsep yang belum saya pahami (misalnya alur MVT) sebelum menerapkannya ke kode, serta menempelkan pesan error PostgreSQL secara langsung untuk didiagnosis penyebabnya.
 
**Keterbatasan AI yang saya temukan:** Untuk debugging error database, AI kadang perlu informasi tambahan (seperti isi file `.env` atau versi PostgreSQL) untuk memberi solusi yang tepat sehingga perlu debugging manual.

### Tugas 3
Saya menggunakan **Github Copilot** sebagai bantuan selama mengerjakan tugas ini, dengan rincian sebagai berikut:
 
**Bagian yang dibantu AI:**
1. Membantu dalam mengembangkan fitur category pada section experience dan skills supaya lebih interaktif.
2. Membantu debugging, terutama ketika berurusan dengan beberapa file Django, seperti `urls.py` dan `models.py`.
4. Penyusunan pesan commit mengikuti format Conventional Commits.

**Strategi prompting:** Saya memberikan potongan kode HTML/CSS dengan framework Django saya secara langsung, lalu menanyakan AI tentang penyebab bug secara spesifik dan optimasi yang bisa dilakukan.
 
**Keterbatasan AI yang saya temukan:** AI beberapa kali men-generate code yang tidak sesuai sehingga menyebabkan website yang dihasilkan kurang enak untuk dilihat. Selain itu, AI juga beberapa kali kurang paham mengenai konteks project secara keseluruhan sehingga perlu intervensi dari saya.

### Tugas 4
Saya menggunakan **Google Antigravity** sebagai bantuan selama mengerjakan tugas ini, dengan rincian sebagai berikut:
 
**Bagian yang dibantu AI:**
1. Membantu penyusunan logika otorisasi server-side (`@login_required`, pengecekan group `Editor`, dan `PermissionDenied`) serta penyesuaian kondisional tombol pada template.
2. Membantu merancang unit test komprehensif di `main/tests.py` untuk menguji hak akses 4 peran pengguna dan fitur toggle star.

**Strategi prompting:** Memberikan spesifikasi checklist izin akses secara langsung dan menempelkan pesan error traceback dari terminal agar diagnosis solusi tepat sasaran.

**Keterbatasan AI yang saya temukan & Analisis Kritis:**
1. **Pencemaran Data Lokal**: AI sempat mengeksekusi fungsi setup pengujian di shell pada database lokal `db.sqlite3` sehingga memunculkan data duplikat pada Experience dan Awards, yang akhirnya harus saya bersihkan manual melalui query ORM.
2. **Crash Django Admin di Python 3.14**: Terjadi error `AttributeError` pada `BaseContext.__copy__` karena perubahan standar library Python 3.14. AI awalnya salah mengira bug berasal dari model fields, sehingga perlu investigasi traceback mendalam sebelum akhirnya diperbaiki dengan menambahkan patch adapter di `portofolio/__init__.py`.
