Nama : Rayhan Fairuz Aqram <br>
NPM : 2506586186 <br>
Kelas : PBP D <br>
Hobi : Olahraga <br>

## Reflective Questions
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

## AI Disclosure
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


