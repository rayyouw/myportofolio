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

#### **Tugas 5: AJAX, Debouncing, Modal, Toast, & XSS Protection**
- Menerapkan pola AJAX Tutorial 05 pada section **Awards**: halaman menampilkan skeleton lalu mengambil data dari `/api/awards/` melalui `fetch()` dan `JsonResponse`.
- Menampilkan loading, empty, dan error state serta mencari award berdasarkan judul dengan debounce 300 ms.
- Superuser dapat menambahkan award melalui modal dan Fetch API. Endpoint memvalidasi `AwardsForm`, memeriksa izin di server, menerima CSRF token, dan mengembalikan JSON dengan status yang sesuai. Daftar award diperbarui tanpa reload.
- Endpoint daftar award tetap dapat dibaca pengunjung anonim dan menyertakan `star_count` serta `is_starred` berdasarkan pengguna yang sedang login.
- Menampilkan toast sukses dan gagal, termasuk pesan validasi dari server. `AwardsForm` membersihkan judul/deskripsi dengan `strip_tags`; teks dari JSON di-escape dengan `escapeHtml` sebelum dirender.
- Menambahkan automated tests untuk skeleton halaman, akses JSON tiap role, state Star per pengguna, otorisasi penambahan award, dan pembersihan input.

#### **Tutorial 7: Django REST Framework**
- Menambahkan API Projects berversi di `/api/v1/projects/` dengan serializer, validasi input, dan permission berbasis superuser.
- Mendukung list/search, detail, create, update, delete, serta toggle star melalui HTTP method REST yang sesuai.
- Mengalihkan halaman Projects ke API DRF dengan CSRF, debounce search, state loading/error/empty, dan refresh AJAX setelah perubahan.
- Menambahkan `APITestCase` untuk akses publik, otorisasi, validasi, CRUD, pencarian, dan star.

#### **Tugas 6: Django REST Framework Implementation (Awards Section)**
- Mengimplementasikan `AwardSerializer` (`ModelSerializer`) dengan daftar `fields` eksplisit, validasi sanitasi teks via `strip_tags` pada `validate_title` dan `validate_description`, serta read-only computed fields (`star_count`, `is_starred`, `starred_by_names`).
- Menerapkan permission class `IsPortfolioOwnerOrEditorOrReadOnly` pada endpoint koleksi dan detail Awards di `/api/v1/awards/`, yang menegakkan hak akses 4 peran (Visitor, Regular User, Editor, Owner) di tingkat permission sebelum request mencapai badan view.
- Menyediakan endpoint function-based API view dengan decorator `@api_view`, `SessionAuthentication`, dan HTTP status codes yang sesuai: 200 OK, 201 Created, 204 No Content, 400 Bad Request, 403 Forbidden, 404 Not Found, dan 405 Method Not Allowed.
- Mengintegrasikan antarmuka Awards (`awards.html`) dengan Fetch API ke endpoint DRF `/api/v1/awards/`: loading/empty/error states, debounce search 300 ms, modal tambah untuk superuser, tombol toggle star dinamis untuk pengguna login, penghapusan data untuk superuser, serta modal edit in-place dan halaman edit untuk Editor dan Superuser tanpa reload halaman.
- Menampilkan toast notifikasi untuk keberhasilan aksi maupun penanganan galat API (400 validation error & 403 authorization error), serta memastikan header `X-CSRFToken` dikirim pada setiap mutasi data.
- Menulis rangkaian pengujian otomatis `AwardAPITest` (`APITestCase`) mencakup 11 test methods yang memvalidasi otorisasi 4 peran, verifikasi jumlah & kondisi data di database, pengujian validasi & sanitasi input, fitur star, computed fields, dan pengujian proteksi CSRF menggunakan `enforce_csrf_checks=True`.

---

# 2. Reflective Questions

### Tugas 1
 
**1. Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti `<section>`, `<article>`, atau `<aside>`? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?**
 
Jawab: Ya saya menggunakan beberapa elemen semantik HTML5, seperti `<header>`, `<nav>`, `<section>`, `<article>`, dan `<footer>`, tetapi tidak menggunakan `<aside>` karena saya tidak menggunakan sidebar. Saya menggunakan `<header>` untuk bagian navbar (username, menu navigasi, dan toggle dark/light), `<nav>` untuk link-link di menu navigasi (Profile, Education, Experience, Awards, dan Skills) di dalam `<header>`, `<section>` untuk pembatas tiap-tiap bagian utama (hero/profile, education, experience, awards, dan skills), `<article>` untuk satu entri konten di dalam setiap section, misalnya satu entri experience atau satu entri awards, serta saya menggunakan `<footer>` sebagai bagian penutup halaman berisi copyright. Elemen-elemen ini mempermudah struktur kode sehingga lebih mudah dibaca dibandingkan hanya menggunakan `<div>` generik.
 
**2. Ketika Anda mengatur CjSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?**
 
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

### Tugas 5

1. **Jelaskan apa itu *debouncing* dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!**

   *Debouncing* adalah teknik menunda eksekusi suatu fungsi sampai tidak ada input baru selama jangka waktu tertentu. Pada pencarian Awards, permintaan baru dikirim 300 milidetik setelah pengguna berhenti mengetik. Tanpa debouncing, setiap karakter yang diketik pengguna akan memicu fungsi pencarian. Misal, pengguna mengetik kata "National", maka aplikasi akan mengirimkan 8 permintaan AJAX sekaligus ke server (N, Na, Nat, Nati, Natio, Nation, Nationa, National). Dengan *debouncing*, browser tidak mengirim permintaan untuk setiap huruf yang diketik sehingga beban server berkurang dan hasil pencarian mengikuti kata kunci terbaru.

2. **Jelaskan fungsi dari penggunaan `await` ketika kita menggunakan `fetch()`! Apa yang akan terjadi jika kita tidak menggunakan `await`?**

   `fetch()` bekerja secara asinkron dan mengembalikan sebuah `Promise`. `await` menunggu sampai `Promise` tersebut selesai sehingga kode dapat memeriksa respons dan membaca JSON sebelum menggunakan datanya. Tanpa `await` atau rangkaian `.then()`, kode langsung menerima objek `Promise`, bukan data respons. Akibatnya, kode yang mencoba membaca isi respons dapat berjalan terlalu cepat sebelum data tersedia.

3. **Jelaskan apa itu serangan XSS (*Cross-Site Scripting*) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui *template* Django!**

   XSS adalah serangan ketika data yang tidak tepercaya ditafsirkan sebagai HTML atau JavaScript aktif di browser pengguna. Template Django secara otomatis melakukan *escaping* pada variabel secara default. Sebaliknya, data JSON yang dimasukkan ke halaman oleh JavaScript tidak otomatis mendapat perlindungan tersebut, terutama jika dimasukkan menggunakan `innerHTML`. Oleh karena itu, nilai yang ditampilkan melalui JavaScript perlu di-*escape* dengan `escapeHtml` atau ditampilkan memakai `textContent`. Pada proyek ini, teks judul dan deskripsi juga dibersihkan di server dengan `strip_tags` sebagai lapisan tambahan.

### Assignment 6

1. **Jelaskan apa arti REST dan mengapa mengembalikan JSON saja tidak cukup untuk menyebut suatu API bersifat RESTful! Jelaskan juga perbedaan antara PUT dan PATCH beserta contoh kapan masing-masing harus digunakan!**

   REST (*Representational State Transfer*) adalah gaya arsitektur (*architectural style*) untuk merancang web API yang berpusat pada konsep **resource**. Mengembalikan data berformat JSON saja belum tentu membuat API tersebut RESTful karena REST menuntut prinsip-prinsip arsitektural tertentu, antara lain:
   - **Resource-based URIs**: Setiap data/kumpulan data diidentifikasi melalui URI yang menunjuk ke *resource* (kata benda), seperti `/api/v1/awards/` untuk koleksi dan `/api/v1/awards/1/` untuk entri tunggal, bukan berupa aksi (seperti `/create-award/` atau `/delete-award/`).
   - **Penggunaan HTTP Method yang Semantik**: Aksi ditentukan oleh metode HTTP (`GET` untuk membaca, `POST` untuk membuat baru, `PUT`/`PATCH` untuk memperbarui, dan `DELETE` untuk menghapus), bukan diletakkan pada nama URL.
   - **Pertukaran Representasi Data**: Klien dan server bertukar representasi data (seperti JSON), bukan objek internal bahasa pemrograman atau baris database mentah.
   - **Stateless**: Setiap permintaan membawa seluruh informasi dan kredensial yang dibutuhkan server tanpa bergantung pada penyimpanan status sesi di server (*session state*) untuk mengetahui konteks permintaan sebelumnya.

   **Perbedaan PUT dan PATCH:**
   - **PUT** bersifat penggantian penuh (*full replacement/update*). Klien mengirimkan representasi lengkap dari resource termasuk seluruh *field* wajib. Jika ada *field* opsional yang diabaikan, nilainya dapat di-reset atau dikosongkan sesuai definisi serializer. Contoh penggunaan: Ketika pengguna ingin memperbarui seluruh entri award secara menyeluruh melalui form komprehensif yang memuat `title`, `description`, dan `thumbnail`.
   - **PATCH** bersifat pembaruan parsial (*partial update*). Klien hanya mengirimkan *field* spesifik yang ingin diubah tanpa harus menyertakan *field* lainnya (`partial=True` pada DRF). Contoh penggunaan: Mengubah hanya judul award (`title`) tanpa perlu menyertakan kembali nilai `description` dan `thumbnail` yang sudah ada sebelumnya.

2. **Jelaskan peran *serializer* pada Django REST Framework! Apa kelebihannya dibandingkan menyusun dictionary secara manual dengan `JsonResponse` seperti pada Tutorial 05?**

   *Serializer* dalam Django REST Framework bertindak sebagai jembatan dua arah (*two-way transformer*) antara tipe data kompleks Django (seperti QuerySet dan model instances) dengan format data standar yang dapat dirender ke JSON/XML (dan sebaliknya).
   - **Serialization (Read/Outgoing)**: Mengonversi objek model Django ke dalam tipe data Python primitif (`dict`, `list`) yang kemudian dirender menjadi respons JSON oleh DRF.
   - **Deserialization & Validation (Write/Incoming)**: Menerima data masukan mentah dari request klien (`request.data`), memvalidasi tipe data, batas panjang, keunikan, hingga sanitasi teks kustom (`validate_<field>`), lalu menyimpan instance ke database melalui metode `.save()`.

   **Kelebihan Serializer dibanding `JsonResponse` manual (Tutorial 05):**
   - **Otomatisasi & Konsistensi Validasi**: Serializer menyediakan validasi bawaan berbasis model skema (`ModelSerializer`) serta validasi per-field yang terpusat dan konsisten, mengembalikan pesan galat terstruktur standar `{field: [errors]}` secara otomatis via `is_valid(raise_exception=True)`.
   - **Dua Arah (Deserialisasi & Serialisasi)**: Pada Tutorial 05, kita harus menyusun dictionary satu per satu saat membaca data, dan memvalidasi form secara terpisah saat menulis data. Serializer menyatukan kontrak data baca dan tulis dalam satu kelas deklaratif.
   - **Dukungan Computed Fields & Relasi**: Memudahkan kalkulasi nilai dinamis (seperti `SerializerMethodField` untuk `star_count` dan `is_starred`) dan menangani relasi antar-model secara efisien dengan context request.
   - **Content Negotiation & Browsable API**: Serializer menghasilkan Python native data yang kompatibel dengan berbagai renderer DRF (JSON, Browsable API HTML form) tanpa perlu `json.dumps()` manual.

3. **Jelaskan perbedaan antara autentikasi (*authentication*) dan otorisasi (*authorization*) pada Django REST Framework! Mengapa hak akses harus diperiksa dengan *permission class* di server, bukan hanya dengan menyembunyikan tombol pada template?**

   - **Autentikasi (*Authentication*)**: Menjawab pertanyaan *"Siapa Anda?"* (*Who are you?*). DRF menggunakan *authentication class* (seperti `SessionAuthentication`) untuk mengidentifikasi pengguna yang mengirimkan request berdasarkan kredensial (misalnya session cookie). Hasilnya adalah menetapkan `request.user` menjadi pengguna terdaftar atau `AnonymousUser`.
   - **Otorisasi (*Authorization*)**: Menjawab pertanyaan *"Apakah Anda diizinkan melakukan tindakan ini?"* (*What are you allowed to do?*). DRF menggunakan *permission class* (seperti `IsPortfolioOwnerOrEditorOrReadOnly` atau `IsAuthenticated`) untuk mengevaluasi apakah `request.user` memiliki hak untuk menjalankan aksi pada metode HTTP dan resource yang diminta.

   **Mengapa hak akses harus diperiksa di server via *permission class*?**
   Menyembunyikan tombol di template HTML hanyalah optimasi antarmuka (UI/UX) untuk kenyamanan visual pengguna awam. Klien atau penyerang dapat dengan mudah mem-bypass tampilan UI dengan mengirimkan HTTP request langsung (melalui DevTools Console, `fetch()`, `cURL`, atau Postman) ke URL endpoint (misalnya mengirim request `DELETE` atau `POST`). Tanpa *permission class* di sisi server, server akan mengeksekusi aksi terlarang tersebut. Oleh karena itu, server adalah pemegang otoritas tunggal atas keamanan data (*single source of truth*) yang mutlak harus memvalidasi setiap hak akses request.

4. **Jelaskan mengapa permintaan yang mengubah data tetap membutuhkan token CSRF ketika API menggunakan `SessionAuthentication`! Mengapa pengujian menggunakan `force_authenticate` tidak cukup untuk membuktikan bahwa perlindungan CSRF bekerja?**

   Ketika API menggunakan `SessionAuthentication`, browser secara otomatis melampirkan cookie sesi (`sessionid`) ke setiap HTTP request yang ditujukan ke domain server yang sama (*same-origin*). Hal ini membuka celah serangan **CSRF (*Cross-Site Request Forgery*)**, di mana situs pihak ketiga yang berbahaya dapat memperdaya browser pengguna yang sedang login untuk mengirimkan request mutasi data (misalnya `POST /api/v1/awards/`) tanpa disadari pengguna. Untuk menangkalnya, Django dan DRF mewajibkan header `X-CSRFToken` pada setiap request yang memodifikasi data (POST, PUT, PATCH, DELETE), memastikan request benar-benar berasal dari aplikasi resmi dan bukan pihak ketiga.

   **Mengapa `force_authenticate` tidak cukup?**
   `force_authenticate()` pada DRF test client adalah jalan pintas pengujian hak akses (*authorization bypass helper*) yang secara langsung mengaitkan objek pengguna ke `request.user` tanpa melewati middleware autentikasi Django, tanpa membuat cookie sesi nyata, dan **secara sengaja mengabaikan pemeriksaan CSRF**. Pengujian dengan `force_authenticate` hanya menguji apakah logika izin (*permission*) bekerja ketika identitas pengguna diketahui. Untuk menguji bahwa pertahanan CSRF benar-benar aktif dan menolak request manipulasi data tanpa token, kita harus menggunakan `APIClient(enforce_csrf_checks=True)` bersama metode `.login()`, yang menjalankan alur sesi nyata dan `CsrfViewMiddleware`.

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

### Tugas 5
Saya menggunakan **OpenAI Codex** sebagai AI coding assistant saat meninjau dan memperbaiki implementasi Assignment 5.

**Bagian yang dibantu AI:**
1. Membandingkan section Awards, endpoint JSON, form AJAX, hak akses tiap role, dan perlindungan XSS dengan checklist tugas.
2. Menambahkan toast untuk aksi tambah/hapus award dan Star, lalu memperbarui automated tests agar sesuai dengan alur halaman AJAX dan endpoint JSON.
3. Membantu perbaikan UI yang diminta selama pengerjaan, termasuk tema gelap/terang, keterbacaan toast/Star, tampilan profil dan navbar.
4. Menyusun dokumentasi progres serta jawaban refleksi Assignment 5 di README.

**Strategi prompting dan ringkasan riwayat:** Saya memberikan checklist tugas, screenshot atau pesan kegagalan yang relevan, kemudian meminta Codex membandingkan implementasi dengan kebutuhan dan memverifikasi hasilnya. Prompt utama mencakup permintaan audit checklist, penyelesaian bagian yang belum lengkap, dan pembaruan tes agar mengikuti arsitektur AJAX. Riwayat percakapan lengkap tersedia di chat Codex yang digunakan untuk mengerjakan repositori ini.

**Keterbatasan AI yang ditemukan:** Tes awal masih mengharapkan halaman Awards dan Projects merender data langsung di HTML. Codex perlu diarahkan untuk mengubah tes agar memeriksa skeleton dan endpoint JSON. Pemeriksaan otomatis juga tidak menggantikan pemeriksaan visual dan uji interaksi langsung di browser; hasil UI tetap saya tinjau berdasarkan screenshot dan kebutuhan yang saya berikan.

### Tugas 6
Saya menggunakan **Google Antigravity (Gemini 2.5 Flash / High Thinking)** sebagai AI coding assistant untuk mengimplementasikan Tutorial 07 dan Tugas 6, dengan rincian sebagai berikut:

**Bagian yang dibantu AI:**
1. Membantu perancangan kelas permission deklaratif `IsPortfolioOwnerOrEditorOrReadOnly` di `main/permissions.py` yang memisahkan otorisasi 4 peran (Visitor, Regular User, Editor, Owner/Superuser) langsung pada tahap *permission check* sebelum masuk ke view body.
2. Membantu penyusunan unit test komprehensif pada `main/tests_api.py` (13 tests sesuai spesifikasi Tutorial 07) dan `main/tests_api_awards.py` (11 tests mencakup pengujian role, database state verification, validasi sanitasi `strip_tags`, read-only computed fields, dan pengujian CSRF dengan `enforce_csrf_checks=True`).
3. Mengintegrasikan modal edit interaktif in-place (`edit-award-modal`) dan event delegation pada `templates/awards.html` serta menambahkan routing `api-auth/` untuk Browsable API login.
4. Menyusun jawaban pertanyaan refleksi Tugas 6 dan dokumentasi progres mingguan.

**Strategi prompting:** Memberikan instruksi spesifik berdasarkan silabus resmi PBP Fasilkom UI (Tutorial 07 dan Individual Assignment 6), mencantumkan checklist kriteria penilaian (rubrik 4/4), serta memvalidasi setiap tahapan dengan menjalankan `python manage.py test main`.

**Keterbatasan AI yang ditemukan & Analisis Kritis:**
1. **Deteksi Versi DRF**: Pada spesifikasi tutorial disebutkan `djangorestframework~=3.18.3`, namun AI mengidentifikasi bahwa rilis DRF di PyPI untuk kompatibilitas Django 4.2 LTS adalah seri 3.15.x. Memaksakan 3.18.3 akan merusak dependensi deployment PWS yang menggunakan Django 4.2, sehingga dilakukan mitigasi mempertahankan `djangorestframework>=3.14,<3.16` di `requirements.txt`.
2. **Pemisahan Logika Otorisasi**: Implementasi awal sempat meletakkan pengecekan `if not request.user.is_superuser` di dalam badan view fungsi `award_list` dan `award_detail`. Hal ini menyalahi kriteria kode bersih DRF (rubrik code quality 3.5-4.0). AI kemudian diarahkan untuk memindahkan seluruh aturan hak akses role Editor dan Owner ke dalam `has_permission()` pada kelas permission `IsPortfolioOwnerOrEditorOrReadOnly`, sehingga view body tetap murni hanya menangani serialisasi dan respons.

