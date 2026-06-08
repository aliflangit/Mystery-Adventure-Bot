import time
import sys
import random
import json
import os
from datetime import datetime

# ==================== ASCII ART ====================
ASCII_PEDANG = """
    ⚔️  KEMENANGAN! ⚔️
    
       /\_/\\
      ( o.o )
       > ^ <
      /|   |\\
     (_|   |_)
    
    ═══════════════════
        SELAMAT!
    ═══════════════════
"""

ASCII_TENGKORAK = """
    💀 KEKALAHAN! 💀
    
                       ______
                    .-"      "-.
                   /            \
       _          |              |          _
      ( \         |,  .-.  .-.  ,|         / )
       > "=._     | )(__/  \__)( |     _.=" <
      (_/"=._"=._ |/     /\     \| _.="_.="\_)
             "=._ (_     ^^     _)"_.="
                 "=\__|IIIIII|__/="
                _.="| \IIIIII/ |"=._
      _     _.="_.="\          /"=._"=._     _
     ( \_.="_.="     `--------`     "=._"=._/ )
      > _.="                            "=._ <
     (_/                                    \_)'
    
    ═══════════════════
     GAME OVER
    ═══════════════════
"""

# Fungsi Dramatis untuk menampilkan teks dengan jeda
def tampilkan_teks(teks, kecepatan=0.05):
    """Menampilkan teks dengan efek ketikan dramatis"""
    for karakter in teks:
        sys.stdout.write(karakter)
        sys.stdout.flush()
        time.sleep(kecepatan)
    print()

def tampilkan_narasi(narasi):
    """Menampilkan narasi cerita dengan jeda antar paragraf"""
    tampilkan_teks(narasi, kecepatan=0.03)
    time.sleep(0.8)

def tampilkan_pilihan(pilihan1, pilihan2):
    """Menampilkan dua pilihan keputusan"""
    print("\n[1] " + pilihan1)
    print("[2] " + pilihan2)
    print()

def input_pilihan():
    """Mengambil input pemain dengan validasi"""
    while True:
        pilihan = input("Pilihan mu (1/2): ").strip()
        if pilihan in ['1', '2']:
            return pilihan
        print("Input tidak valid! Masukkan 1 atau 2.")

# Variabel Global
nyawa = 100
nama_pemain = ""

def tampilkan_status(nyawa):
    """Menampilkan status kesehatan pemain"""
    print(f"\n❤️  Nyawa: {nyawa}/100")
    if nyawa <= 20:
        tampilkan_teks("⚠️  PERINGATAN: Nyawa mu hampir habis!", kecepatan=0.08)
    print()

# ==================== SISTEM SAVE FILE ====================
SAVE_FILE = "game_saves.json"

def simpan_data_pemain(nama, nyawa, ending, waktu_bermain):
    """Simpan data pemain ke file JSON"""
    data_game = {
        "nama": nama,
        "nyawa_akhir": nyawa,
        "ending": ending,
        "waktu_bermain": waktu_bermain,
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Load data lama jika ada
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            try:
                data_lama = json.load(f)
                if not isinstance(data_lama, list):
                    data_lama = [data_lama]
            except:
                data_lama = []
    else:
        data_lama = []
    
    # Tambah data baru
    data_lama.append(data_game)
    
    # Simpan ke file
    with open(SAVE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data_lama, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Data permainan disimpan ke {SAVE_FILE}")

def lihat_riwayat_permainan():
    """Tampilkan riwayat permainan"""
    if not os.path.exists(SAVE_FILE):
        print("\n📋 Belum ada riwayat permainan.")
        return
    
    with open(SAVE_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            print("\n" + "="*50)
            print("📋 RIWAYAT PERMAINAN")
            print("="*50)
            for i, pemain in enumerate(data, 1):
                print(f"\n🎮 Permainan #{i}:")
                print(f"   Nama: {pemain.get('nama', 'Unknown')}")
                print(f"   Nyawa Akhir: {pemain.get('nyawa_akhir', 0)}/100")
                print(f"   Ending: {pemain.get('ending', 'Unknown')}")
                print(f"   Waktu: {pemain.get('tanggal', 'Unknown')}")
            print("\n" + "="*50 + "\n")
        except:
            print("\n❌ Error membaca riwayat permainan.")


def awal_cerita(nama):
    """Karakter setup dan jalur awal cerita"""
    global nyawa
    nyawa = 100
    
    tampilkan_narasi(
        "Anda terbangun di sebuah lorong yang gelap dan dingin. Bangunan tua ini tercakup "
        "debu dan sarang laba-laba. Lampu neon yang rusak berkedip-kedip di atas kepala, "
        "menciptakan bayangan yang menari-nari di dinding. Anda tidak ingat bagaimana bisa sampai di sini. "
        "Telinga Anda mendengarkan suara aneh - seperti bisikan yang tidak jelas dari kegelapan."
    )
    
    tampilkan_teks(f"Nama Anda: {nama}", kecepatan=0.04)
    tampilkan_status(nyawa)
    
    tampilkan_narasi(
        "Anda menemukan dua jalan. Di sebelah kiri, cahaya merah membocor dari celah pintu "
        "yang bertuliskan 'LEMBAH CODING - ZONA AMAN BERLABEL'. Di sebelah kanan, "
        "tebing batu setinggi langit menjulang gelap. Tidak ada petunjuk jalan, hanya "
        "simbol di batunya: 'GUNUNG BUG - JANGAN MASUK'. Napas Anda menjadi berat. "
        "Pilihan pertama terasa aman tapi mencurigakan. Pilihan kedua... entahlah."
    )
    
    tampilkan_pilihan(
        "Masuk ke Lembah Coding (jalan yang cahaya)",
        "Mendaki Gunung Bug (mengabaikan peringatan)"
    )
    
    pilihan = input_pilihan()
    
    if pilihan == '1':
        lembah_coding(nama)
    else:
        gunung_bug(nama)

# ==================== JALUR 1: LEMBAH CODING ====================
def lembah_coding(nama):
    """Jalur pertama - Lembah Coding"""
    global nyawa
    
    tampilkan_narasi(
        "Anda memasuki pintu merah dengan hati-hati. Di dalam, pemandangan yang aneh menanti. "
        "Anda berada di ruangan besar dengan layar komputer berjejer-jejer. Semua laptop itu "
        "masih menyala, layarnya menampilkan kode yang terus berubah. Udara terasa panas dan "
        "tercium bau listrik yang terbakar. Di sudut ruangan, Anda melihat sesosok manusia yang duduk "
        "di depan komputer - tidak bergerak. Dia seperti boneka yang hidup sebentar tapi tidak sepenuhnya manusia."
    )
    
    tampilkan_status(nyawa)
    
    tampilkan_narasi(
        "Sosok itu tiba-tiba menoleh ke arah Anda. Matanya kosong, tanpa kehidupan. Dia berkehelek: "
        "'Welcome... New_Programmer_001.exe'. Anda merasa punggung Anda mendingin. Setiap layar komputer "
        "sekarang menampilkan wajah Anda sendiri, tapi dengan ekspresi gila. Anda menyadari - "
        "ini adalah jebakan. Anda adalah target berikutnya."
    )
    
    tampilkan_pilihan(
        "Cari cara keluar - mencari pintu atau jendela",
        "Dekati sosok itu dan tanyakan apa yang terjadi"
    )
    
    pilihan = input_pilihan()
    
    if pilihan == '1':
        lembah_cari_keluar(nama)
    else:
        lembah_dekati_sosok(nama)

def lembah_cari_keluar(nama):
    """Cabang: Mencari keluar dari Lembah Coding (dengan elemen randomness)"""
    global nyawa
    
    tampilkan_narasi(
        "Anda berlari ke sudut ruangan. Tangan Anda menyentuh dinding dingin dan basah. "
        "Anda menemukan jendela, tapi semuanya tertutup rapat oleh papan kayu yang terpaku. "
        "Sementara itu, sosok aneh itu mulai berjalan ke arah Anda dengan langkah yang tidak normal. "
        "Kepalanya berputar-putar. Anda mendengar suara berderit yang menyeramkan dari tulang-tulangnya."
    )
    
    tampilkan_narasi(
        "Di meja dekat Anda, ada pemecah kaca darurat berkilau merah. Tapi di sudut lain, "
        "Anda melihat pintu layanan yang sudah setengah terbuka. Melalui celah itu, Anda bisa "
        "melihat tangga yang menuju ke tempat yang lebih terang. Sosok itu semakin dekat..."
    )
    
    tampilkan_status(nyawa)
    
    tampilkan_pilihan(
        "Ambil pemecah kaca dan buat jalan keluar",
        "Berlari ke pintu layanan dan naik tangga"
    )
    
    pilihan = input_pilihan()
    
    if pilihan == '1':
        # Tambah randomness: 60% berhasil, 40% gagal
        kesuksesan = random.random() < 0.6
        
        if kesuksesan:
            tampilkan_narasi(
                "Anda mengambil pemecah kaca dengan tangan yang tenang. Anda berfokus dan "
                "memukul jendela dengan keras. CRACK! Jendela pecah menjadi ribuan kepingan. "
                "Sosok itu berteriak dari jauh di belakang. Anda melewati celah jendela yang tajam "
                "dan terjatuh ke luar. Meskipun lama jatuhnya, Anda merasakan tanah yang lembut menghampiri Anda."
            )
            tampilkan_status(nyawa)
            akhir_selamat(nama, "SELAMAT & BERANI")
        else:
            nyawa -= 20
            tampilkan_narasi(
                "Anda mengambil pemecah kaca dengan tangan yang gemetar. Anda memukul jendela, "
                "tapi kaca itu sangat tebal! Pukulan Anda hanya membuat retakan kecil. "
                "Sosok itu sudah mencapai Anda! Tangan dinginnya menangkap leher Anda. "
                "Anda berhasil keluar dengan sesuatu yang menelepon dari dalam ruangan, "
                "tapi Anda terluka parah."
            )
            tampilkan_status(nyawa)
            if nyawa > 0:
                akhir_tersembunyi(nama, "SELAMAT DENGAN LUKA")
            else:
                game_over(nama, "KEKALAHAN - TERLALU TERLAMBAT")
    else:
        tampilkan_narasi(
            "Anda berlari dengan cepat ke pintu layanan dan mendorong tugasnya dengan sekuat tenaga. "
            "Pintu itu terbuka dengan teriakan yang tajam - seperti pipa uap yang meledak. "
            "Anda naik tangga berliku dengan napas tersengal-sengal. Di belakang Anda, "
            "suara langkah sosok itu semakin menjauh. Anda berhasil menemukan ruang yang terang dan "
            "menutup pintu di belakang Anda dengan menggerakkan lemari besar untuk menghalanginya."
        )
        tampilkan_status(nyawa)
        akhir_selamat(nama, "SELAMAT DENGAN STRATEGI")


def lembah_dekati_sosok(nama):
    """Cabang: Dekati sosok aneh di Lembah Coding"""
    global nyawa
    nyawa -= 20
    
    tampilkan_narasi(
        "Anda melangkah perlahan ke arah sosok itu. Demi Tuhan, aromanya... seperti kabel yang hangus "
        "dan daging yang membusuk. Matanya yang kosong memandang Anda dengan intens. "
        "Dia membuka mulutnya, dan terdengar suara yang bersamar seperti ASCII - "
        "seperti pesan error: 'System_Corruption... Cannot_Find_Exit... Assimilate_Consciousness.exe'."
    )
    
    tampilkan_narasi(
        "Sosok itu menjulurkan tangan ke arah Anda. Saat jari-jarinya hampir menyentuh tubuh Anda, "
        "tiba-tiba semua layar di ruangan bergoyang dan mati. Dalam gelap total, Anda mendengar "
        "terengah-engah manusia dan suara klik-klik dari keyboard fantom. Sesuatu bergerak di kegelapan. "
        "Anda merasa dirinya diikuti."
    )
    
    tampilkan_status(nyawa)
    
    tampilkan_pilihan(
        "Berlari meninggalkan ruangan tanpa tujuan",
        "Berdiri diam dan berkonsentrasi untuk menemukan penyelamat"
    )
    
    pilihan = input_pilihan()
    
    if pilihan == '1':
        nyawa -= 20
        tampilkan_narasi(
            "Anda berlari buta dalam kegelapan. Kepala Anda menabrak sesuatu yang keras dan Anda jatuh. "
            "Saat sadar, Anda menemukan diri Anda terperangkap dalam sebuah ruangan kecil yang "
            "penuh dengan hard disk yang menggerayang. Ini adalah hati dari sistem. "
            "Tidak ada jalan keluar..."
        )
        tampilkan_status(nyawa)
        if nyawa > 0:
            akhir_terjebak(nama, "TERJEBAK DI HATI SISTEM")
        else:
            game_over(nama, "KEKALAHAN - TERTABRAK")
    else:
        tampilkan_narasi(
            "Anda menutup mata dan menarik napas dalam-dalam. Dalam pikiran Anda, "
            "Anda membayangkan cahaya, kehangatan, rumah Anda. Tiba-tiba, sebuah kilatan merah menerangi ruangan. "
            "Sosok itu berteriak - suara yang tidak manusiawi. Lampu darurat menyala. "
            "Pintu emesi terbuka dengan sendirinya. Ada jalan keluar!"
        )
        tampilkan_status(nyawa)
        akhir_selamat(nama, "SELAMAT DENGAN MEDITASI")

# ==================== JALUR 2: GUNUNG BUG ====================
def gunung_bug(nama):
    """Jalur kedua - Gunung Bug"""
    global nyawa
    nyawa -= 15
    
    tampilkan_narasi(
        "Anda mengabaikan peringatan dan mulai mendaki tebing batu. Batu-batu itu tajam dan "
        "menyebabkan luka di tangan Anda. Semakin tinggi Anda naik, semakin dingin udaranya. "
        "Anda melihat goresan aneh di batu-batu - seperti simbol error handling dan syntax yang tidak lengkap. "
        "Napas Anda membentuk asap di udara yang membeku."
    )
    
    tampilkan_narasi(
        "Di tengah pendakian, Anda menemukan gua dalam yang menerangi. "
        "Dari dalam gua, terdengar suara yang seperti debat antara beberapa programmer yang marah: "
        "'Siapa yang tidak merge branch ini?', 'Kode ini crash!', 'DEBUG! DEBUG!'. "
        "Cahaya aneh keluar dari gua tersebut. Anda juga melihat jalan memutar yang melanjutkan pendakian, "
        "tapi batu-batu itu terlihat tidak stabil."
    )
    
    tampilkan_status(nyawa)
    
    tampilkan_pilihan(
        "Masuk ke gua yang penuh suara aneh",
        "Terus mendaki melewati batu-batu yang tidak stabil"
    )
    
    pilihan = input_pilihan()
    
    if pilihan == '1':
        gunung_gua_aneh(nama)
    else:
        gunung_lanjut_mendaki(nama)

def gunung_gua_aneh(nama):
    """Cabang: Masuk gua dalam di Gunung Bug"""
    global nyawa
    
    tampilkan_narasi(
        "Anda memasuki gua. Dinding-dindingnya bersinar dengan cahaya cyan dan magenta yang aneh. "
        "Di dalam gua, Anda melihat empat 'programmer spiritual' yang tergantung di udara. "
        "Mereka semua tidak memiliki tubuh - hanya kepala yang melayang, dengan ekspresi terkenal dan frustasi. "
        "Saat anda masuk, semua kepala itu menoleh ke arah Anda secara bersamaan."
    )
    
    tampilkan_narasi(
        "Kepala yang tertua berbicara dengan suara yang seperti echo: "
        "'Anda datang untuk menjadi bagian dari eternal debugging, yes?' "
        "Mereka melihat Anda sebagai calon untuk bergabung dengan keabadian mereka. "
        "Di belakang mereka, Anda melihat portal yang bersinar. Tapi ada juga celah kecil di dinding gua "
        "yang mengarah ke lorong gelap yang tidak diketahui."
    )
    
    tampilkan_status(nyawa)
    
    tampilkan_pilihan(
        "Dengarkan proposal mereka dan pertimbangkan bergabung dengan portal",
        "Cepat-cepat masuk ke celah lorong gelap sebelum mereka memblokirmu"
    )
    
    pilihan = input_pilihan()
    
    if pilihan == '1':
        nyawa -= 25
        tampilkan_narasi(
            "Anda mendekat ke portal. Kepala-kepala itu berbeda suara, bercerita tentang dunia "
            "tanpa error, tempat kode selalu sempurna. Anda tergoda oleh visi mereka... "
            "Tapi saat Anda hampir menyentuh portal, Anda melihat ribuan versi diri Anda sendiri "
            "dalam portal, semua frustrasi dan terjebak. Nyawa Anda mengejang dengan deru manik-manik. "
            "Ini bukan keselamatan. Ini adalah penjara eternal."
        )
        tampilkan_status(nyawa)
        if nyawa > 0:
            akhir_tersembunyi(nama, "SELAMAT TAPI TERGODA PORTAL")
        else:
            game_over(nama, "KEKALAHAN - DISERAP PORTAL")
    else:
        tampilkan_narasi(
            "Anda berlari ke celah dan masuk ke lorong gelap dengan kepala-kepala itu mengejar Anda. "
            "Mereka berteriak: 'KEMBALI! KEMBALI!' Lorong itu tiba-tiba membuka ke hutan batu "
            "yang indah dan aneh. Pohon-pohon terbuat dari kode yang bercahaya. "
            "Anda akhirnya menemukan sesuatu yang nyata."
        )
        tampilkan_status(nyawa)
        akhir_bebas(nama, "BEBAS DARI PORTAL")

def gunung_lanjut_mendaki(nama):
    """Cabang: Terus mendaki Gunung Bug"""
    global nyawa
    nyawa -= 10
    
    tampilkan_narasi(
        "Anda melanjutkan pendakian dengan sangat hati-hati. Batu-batu di bawah kaki Anda bergerak-gerak. "
        "Anda dapat mendengar suara retakan dan bongkah batu yang jatuh jauh ke bawah. "
        "Tapi Anda terus maju, dipandu oleh cahaya putih yang semakin terang di puncak."
    )
    
    tampilkan_narasi(
        "Saat Anda hampir mencapai puncak, sebuah tebing besar runtuh. Anda merasakan keseimbangan Anda goyah. "
        "Tapi dengan gerakan cepat, Anda berhasil memegang batu besar dan mengangkat diri Anda ke puncak. "
        "Dari sana, Anda melihat dunia yang luas - bukan lagi bangunan tua yang menakutkan. "
        "Anda melihat kota yang indah, matahari terbit, dan harapan."
    )
    
    tampilkan_status(nyawa)
    
    tampilkan_pilihan(
        "Turun dari gunung dan pergi ke kota",
        "Cari arti dari pencapaian Anda di puncak sebelum pergi"
    )
    
    pilihan = input_pilihan()
    
    if pilihan == '1':
        tampilkan_narasi(
            "Anda turun dari gunung dengan langkah yang ringan. Setiap langkah membuat Anda semakin dekat "
            "dengan kehidupan yang normal. Kota itu menyambut Anda dengan kehangatan dan kesegaran. "
            "Orang-orang normal, udara yang bersih, dan realitas yang memang nyata. Anda telah berhasil melarikan diri."
        )
        tampilkan_status(nyawa)
        akhir_selamat(nama, "SELAMAT KE KOTA")
    else:
        tampilkan_narasi(
            "Anda menerima sebuah batu kecil yang bersinar di puncak gunung. "
            "Ketika Anda menyentuhnya, Anda membayangkan jejak dari semua programmer yang pernah terjebak di sini - "
            "dan semua programmer yang telah berhasil melarikan diri. Anda merasa menjadi bagian dari komunitas pejuang. "
            "Dengan batu aneh ini, Anda merasa memiliki tujuan. Anda turun dengan semangat baru dan memulai petualangan baru."
        )
        tampilkan_status(nyawa)
        akhir_bebas(nama, "BEBAS DENGAN ARTEFAK MISTIS")

# ==================== AKHIR CERITA ====================
def akhir_selamat(nama, tipe_ending="SELAMAT"):
    """Akhir baik - Selamat dari petualangan"""
    tampilkan_narasi(
        f"Halo, {nama}. Anda telah berhasil meloloskan diri dari jebakan digital itu. "
        "Dunia di luar menunggu Anda. Matahari terbit membangunkan kesadaran baru dalam diri Anda. "
        "Anda tidak akan pernah lupa pengalaman ini, tapi Anda telah dipilih untuk hidup."
    )
    tampilkan_teks("==========================================", kecepatan=0.02)
    tampilkan_teks("✨ SELAMAT! ANDA BERHASIL BEBAS! ✨", kecepatan=0.05)
    tampilkan_teks("==========================================", kecepatan=0.02)
    print(ASCII_PEDANG)
    tampilkan_status(nyawa)
    simpan_data_pemain(nama, nyawa, tipe_ending, "Cerita Selamat")

def akhir_bebas(nama, tipe_ending="BEBAS & BIJAKSANA"):
    """Akhir transformasi - Bebas dengan pemahaman baru"""
    tampilkan_narasi(
        f"{nama}, Anda tidak hanya selamat, tapi Anda juga menemukan arti sejati dari "
        "kebebasan dan kehidupan. Dunia digital itu adalah metafora dari ketakutan manusia, "
        "dan Anda telah mengatasinya. Sekarang Anda memahami bahwa realitas adalah apa yang Anda buat."
    )
    tampilkan_teks("==========================================", kecepatan=0.02)
    tampilkan_teks("🌟 ENDING SEMPURNA - KEBEBASAN & KEBIJAKSANAAN! 🌟", kecepatan=0.05)
    tampilkan_teks("==========================================", kecepatan=0.02)
    print(ASCII_PEDANG)
    tampilkan_status(nyawa)
    simpan_data_pemain(nama, nyawa, tipe_ending, "Cerita Bebas")

def akhir_tersembunyi(nama, tipe_ending="SELAMAT TAPI TERLUKA"):
    """Akhir tersembunyi - Selamat tapi dengan luka"""
    tampilkan_narasi(
        f"{nama}, Anda berhasil melarikan diri, tapi dengan biaya yang tinggi. "
        "Anda membawa beban dari dunia itu. Setiap malam, Anda masih mendengar suara-suara aneh. "
        "Apakah Anda benar-benar bebas? Atau apakah itu bagian dari mereka masih melekat pada Anda?"
    )
    tampilkan_teks("==========================================", kecepatan=0.02)
    tampilkan_teks("⚫ ENDING TERSEMBUNYI - SELAMAT TAPI TERLUKA ⚫", kecepatan=0.05)
    tampilkan_teks("==========================================", kecepatan=0.02)
    print(ASCII_PEDANG)
    tampilkan_status(nyawa)
    simpan_data_pemain(nama, nyawa, tipe_ending, "Cerita Tersembunyi")

def akhir_terjebak(nama, tipe_ending="TERJEBAK SELAMANYA"):
    """Akhir - Terjebak selamanya"""
    tampilkan_narasi(
        f"{nama}, Anda telah menjadi bagian dari sistem. Anda adalah bagian dari eternal debugging. "
        "Anda sekarang duduk di depan layar, melihat orang lain dan menunggu pemrogramer berikutnya. "
        "Siklus berulang. Selamanya. Anda telah menjadi error yang hidup selamanya."
    )
    tampilkan_teks("==========================================", kecepatan=0.02)
    tampilkan_teks("💀 GAME OVER - ANDA TERJEBAK SELAMANYA 💀", kecepatan=0.05)
    tampilkan_teks("==========================================", kecepatan=0.02)
    print(ASCII_TENGKORAK)
    tampilkan_status(nyawa)
    simpan_data_pemain(nama, nyawa, tipe_ending, "Cerita Terjebak")

def game_over(nama, tipe_ending="NYAWA HABIS"):
    """Akhir - Nyawa habis"""
    tampilkan_narasi(
        f"{nama}... napas Anda berhenti. Dunia menjadi gelap. Ini adalah akhir dari petualangan Anda. "
        "Apakah Anda benar-benar pernah ada, atau hanya karakter di dalam kode?"
    )
    tampilkan_teks("==========================================", kecepatan=0.02)
    tampilkan_teks("💀 GAME OVER - NYAWA HABIS 💀", kecepatan=0.05)
    tampilkan_teks("==========================================", kecepatan=0.02)
    print(ASCII_TENGKORAK)
    tampilkan_status(nyawa)
    simpan_data_pemain(nama, nyawa, tipe_ending, "Cerita Game Over")

# ==================== FUNGSI UTAMA ====================
def tampilkan_menu_utama():
    """Tampilkan menu utama"""
    print("\n" + "="*50)
    print("🎮 MYSTERY ADVENTURE BOT - MENU UTAMA 🎮")
    print("="*50)
    print("\n[1] Mulai Game Baru")
    print("[2] Lihat Riwayat Permainan")
    print("[3] Keluar dari Game")
    print()

def main_loop():
    """Loop utama permainan dengan opsi main lagi"""
    while True:
        tampilkan_menu_utama()
        
        pilihan = input("Pilihan mu (1/2/3): ").strip()
        
        if pilihan == '1':
            start_game()
        elif pilihan == '2':
            lihat_riwayat_permainan()
        elif pilihan == '3':
            tampilkan_teks("\n👋 Bayar dengan kehidupan... Game telah berakhir.")
            print("="*50)
            break
        else:
            print("Input tidak valid! Masukkan 1, 2, atau 3.")

def start_game():
    """Fungsi untuk memulai game"""
    global nyawa
    
    print("\n" + "="*50)
    print("🎮 SELAMAT DATANG DI MYSTERY ADVENTURE BOT 🎮")
    print("="*50)
    print("\n⚠️  PERHATIAN: Game ini mengandung tema gelap dan menakutkan!")
    print("Siapkan diri Anda untuk petualangan yang tidak akan dilupakan.\n")
    
    time.sleep(1)
    
    global nama_pemain
    nama_pemain = input("Siapa namamu, pemberani? ").strip()
    
    if not nama_pemain:
        nama_pemain = "Traveler"
    
    print()
    tampilkan_teks(f"Baik, {nama_pemain}... Mari kita mulai...", kecepatan=0.05)
    time.sleep(1)
    print()
    
    # Reset nyawa untuk permainan baru
    nyawa = 100
    
    # Mulai cerita
    awal_cerita(nama_pemain)
    
    # Tanya main lagi
    print("\n" + "="*50)
    tanya_main_lagi()

def tanya_main_lagi():
    """Tanya pemain apakah ingin main lagi"""
    while True:
        jawab = input("Main lagi? (y/n): ").strip().lower()
        
        if jawab == 'y':
            start_game()
            break
        elif jawab == 'n':
            tampilkan_teks("\n👋 Terima kasih telah bermain Mystery Adventure Bot!")
            print("="*50 + "\n")
            break
        else:
            print("Input tidak valid! Masukkan 'y' atau 'n'.")

def game_utama():
    """Fungsi utama untuk menjalankan permainan"""
    main_loop()

if __name__ == "__main__":
    game_utama()