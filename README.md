Nama : Rayhan Fairuz Aqram 
NPM : 2506586186 
Kelas : PBP D 
Hobi : Olahraga

### Tugas 1

1. Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti <section>, <article>, atau <aside>? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?

Jawab: Ya saya menggunakan beberapa elemen semantik HTML 5, seperti <header>, <nav>, <section>, <article>, dan <footer>, tetapi tidak menggunakan <aside> karena saya tidak menggunakan sidebar. Saya menggunakan <header> untuk bagian navbar (username, menu navigasi, dan toggle dark/light), <nav> untuk link-link di menu navigasi (Profile, Education, Experience, Awards, dan Skills) di dalam <header>, <section> untuk pembatas tiap-tiap bagian utama(hero/profile, education, experience, awards, dan skills), <article> untuk satu entri konten di dalam setiap section, misalnya satu entri experience atau satu entri awards, serta saya menggunakan <footer> sebagai bagian penutup halaman berisi copyright. Elemen-elemen ini mempermudah struktur kode sehingga lebih mudah dibaca dibandingkan hanya menggunakan <div> generik.

2. Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?

Jawab: Tantangan utama ada di section yang pakai CSS Grid dua kolom (foto + teks), seperti di bagian hero/profile. Di layar sempit, saya ubah grid-template-areas jadi susunan vertikal supaya foto tetap besar dan teks tidak terlalu sempit. Untuk grid di section education, experience, awards, dan skills, saya turunkan dari multi-kolom ke 1 kolom penuh di mobile karena keterbacaan teks lebih saya prioritaskan dibanding efisiensi ruang.

3. Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?

Jawab: Ada beberapa batasan yang saya rasakan. Pertama, section experience dan skills yang awalnya ingin difilter (misalkan: experience dibagi lagi menjadi work dan organisasi/kepanitiaan) menggunakan fungsi :has() di CSS tidak didukung semua browser. Kedua, preferensi dark/light mode juga tidak bisa disimpan lintas sesi tanpa localStorage. Ketiga, form kontak email masih sebatas link mailto: tanpa bisa mengirim langsung. Kedepannya, saya ingin mengatasi batasan-batasan tersebut menggunakan JavaScript dan Backend Tools lainnya supaya website lebih fungsional dan dinamis

### AI Disclosure
Saya menggunakan Claude (Anthropic) sebagai bantuan selama mengerjakan tugas ini, dengan rincian sebagai berikut:

1. Debugging CSS specificity conflict pada fitur filter Experience (rule .experience-item { display: flex } menimpa .timeline-item { display: none }).

2. Perbaikan bug scroll-margin-top supaya judul section tidak tertutup navbar fixed saat diklik dari navigasi.

3. Review kode untuk mendeteksi CSS yang redundan/konflik (misalnya dua deklarasi .hero yang saling menimpa).

4. Penyusunan pesan commit mengikuti format Conventional Commits.

Strategi prompting: Saya memberikan potongan kode HTML/CSS asli saya secara langsung, lalu meminta AI menjelaskan penyebab bug secara spesifik dan optimasi yang bisa dilakukan.

Keterbatasan AI yang saya temukan: Beberapa saran AI kurang match dengan ekspektasi yang saya mau, seperti misalkan membuat foto dan teks sejajar atau mengubah theme color sesuai selera saya. Jadi, saya mengambil kesimpulan bahwa AI belum bisa untuk mengerti secara kompleks kreativitas dari manusia.