import os
import sys
import psycopg2

#fungsi untuk terkoneksi dengan database PostgreSQL
def connectDB():
    try:
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="SuperPower07",
            dbname="sitragu3"
        )
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print("Gagal koneksi ke database:", e)
        return None, None

#fungsi untuk menghentikan sementara program
def pause():
    input("\nTekan ENTER untuk melanjutkan...")

#fungsi untuk keluar dari program
def logout():
    print("\nTerima kasih telah menggunakan SITRAGU. Sampai jumpa!")
    pause()
    sys.exit(0)

#menu utama program
def menu_utama():
    while True : 
        os.system('cls')
        print(r'''                                                    
        ███████ ███████ ██       █████  ███    ███  █████  ████████     ██████   █████  ████████  █████  ███    ██  ██████  
        ██      ██      ██      ██   ██ ████  ████ ██   ██    ██        ██   ██ ██   ██    ██    ██   ██ ████   ██ ██       
        ███████ █████   ██      ███████ ██ ████ ██ ███████    ██        ██   ██ ███████    ██    ███████ ██ ██  ██ ██   ███ 
             ██ ██      ██      ██   ██ ██  ██  ██ ██   ██    ██        ██   ██ ██   ██    ██    ██   ██ ██  ██ ██ ██    ██ 
        ███████ ███████ ███████ ██   ██ ██      ██ ██   ██    ██        ██████  ██   ██    ██    ██   ██ ██   ████  ██████  
                                                                                                                    
                                                                                                                    
                            ██████  ██     ███████ ██ ████████ ██████   █████   ██████  ██    ██                    
                            ██   ██ ██     ██      ██    ██    ██   ██ ██   ██ ██       ██    ██                    
                            ██   ██ ██     ███████ ██    ██    ██████  ███████ ██   ███ ██    ██                    
                            ██   ██ ██          ██ ██    ██    ██   ██ ██   ██ ██    ██ ██    ██                    
                            ██████  ██     ███████ ██    ██    ██   ██ ██   ██  ██████   ██████                     
                                                                                                                    
                                                                                                                                                                                                                                                       
        ''')
        print("1. Registrasi") 
        print("2. Login")
        print("3. Log out")

        pilih = input("Masukkan pilihan (1-3): ").strip()
        if pilih == '1': 
            registrasi() #pindah ke menu registrasi
        elif pilih == '2':
            login()      #pindah ke menu login
        elif pilih == '3':
            logout()     #keluar dari aplikasi
            break
        else:
            print("Pilihan tidak valid.")
            pause()

# fungsi registrasi pengguna baru
def registrasi():
    conn, cur = connectDB()
    if not conn:
        pause()
        return

    try:
        os.system('cls')
        print(r'''
        =============================================
                      REGISTRASI BOS            
        =============================================''')
        
        # input data user
        nama = input("Nama : ").strip().title()
        email = input("Email : ").strip().lower()
        password = input("Password : ").strip()
        
        # validasi input nomer telepon
        while True:
            no_telepon = input("No telepon : ").strip()
            if no_telepon.isdigit():
                break
            print("No telepon hanya boleh angka!")
        
        # cek apakah email sudah pernah digunakan
        cur.execute("SELECT email FROM pengguna WHERE email=%s", (email,))
        if cur.fetchone():
            print("\nEmail sudah digunakan!")
            pause()
            return
        
        # insert user baru apakah sebagai pelanggan default
        cur.execute(
            "INSERT INTO pengguna (nama_pengguna, email, password, no_telepon, role) VALUES (%s, %s, %s, %s, %s)",
            (nama, email, password, no_telepon, 'pelanggan')
        )
        conn.commit()
        print("\nPendaftaran berhasil!")

    except Exception as e:
        print("Terjadi kesalahan saat registrasi:", e)
    finally:
        cur.close()
        conn.close()

    pause()

# fungsi login pengguna
def login():
    os.system('cls')
    print(r'''
    =============================================
                 BANG LOGIN BANG            
    =============================================''')

    email = input("Email : ").strip().lower()
    password = input("Password : ").strip()

    conn, cur = connectDB()
    if not conn:
        pause()
        return

# cek email dan password
    try:
        cur.execute(
            "SELECT id_user, role FROM pengguna WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cur.fetchone()

        if not user:
            print("Email atau password salah!")
            pause()
            return
# cek role user, admin atau pelanggan
        if user[1] == 'admin':
            print("\nLogin berhasil. Selamat datang admin!")
            pause()
            menu_admin() # menu khusus admin
        else:
            print("\nLogin berhasil sebagai pelanggan!")
            pause()
            menu_user(user[0]) # menu khusus pelanggan

    except Exception as e:
        print("Login gagal!", e)
    finally:
        cur.close()
        conn.close()

# menu admin
def menu_admin():
    while True:
        os.system('cls')
        print(r'''
        =============================================
                         MENU ADMIN           
        =============================================''')
        print('1. Kelola Bahan Baku')
        print('2. Kelola Produk')
        print('3. Daftar Permintaan (Pesanan)')
        print('4. Status Pesanan')
        print('5. Riwayat Transaksi')
        print('6. Logout')

        pilih = input('Masukkan pilihan (1-6): ').strip()

        if pilih == '1':
            kelola_bahan_baku()
        elif pilih == '2':
            kelola_produk()
        elif pilih == '3':
            daftar_permintaan()
        elif pilih == '4':
            status_pesanan()
        elif pilih == '5':
            riwayat_transaksi()
        elif pilih == '6':
            break
        else:
            print("Pilihan tidak valid.")
            pause()

# admin kelola stok bahan baku
def kelola_bahan_baku():
    conn, cur = connectDB()
    if not conn:
        pause()
        return

    try:
        os.system('cls')
        print(r'''
        =============================================
                      KELOLA BAHAN BAKU            
        =============================================''')

        # ambil data laporan terbaru
        cur.execute("""
            SELECT id_laporan, jumlah_bahan_baku
            FROM laporan
            ORDER BY id_laporan DESC
            LIMIT 1
        """)
        data = cur.fetchone()

        if not data:
            print("Tidak ada laporan ditemukan!")
            pause()
            return

        id_laporan, jumlah_bahan_baku = data
        print(f"Jumlah Bahan Baku Saat Ini : {jumlah_bahan_baku}")
        
        # tambah stok
        tambah = input("\nMasukkan jumlah bahan baku baru yang ingin ditambahkan: ").strip()
        if not tambah.isdigit():
            print("Input harus berupa angka!")
            pause()
            return
        tambah = int(tambah)
        
        # Update jumlah_bahan_baku pada tabel laporan
        cur.execute("""
            UPDATE laporan
            SET jumlah_bahan_baku = jumlah_bahan_baku + %s
            WHERE id_laporan = %s
        """, (tambah, id_laporan))
        conn.commit()

        print("\nBahan baku berhasil ditambahkan!")
        print(f"Total bahan baku sekarang: {jumlah_bahan_baku + tambah}")

    except Exception as e:
        print("Terjadi kesalahan:", e)
    finally:
        cur.close()
        conn.close()

    pause()

# fungsi untuk mengelola produk
def kelola_produk():
    conn, cur = connectDB()
    if not conn:
        pause()
        return

    try:
        while True:
            os.system('cls')
            print(r'''
            =============================================
                             DAFTAR PRODUK            
            =============================================''')
            # Ambil semua produk yang tidak dihapus (is_deleted = FALSE)
            cur.execute("SELECT id_produk, nama_produk, harga, stok FROM produk WHERE is_deleted = FALSE ORDER BY id_produk ASC")
            produk = cur.fetchall()
            
            # Tampilkan daftar produk
            for p in produk:
                print(f"{p[0]}. {p[1]} - Rp {p[2]} (Stok: {p[3]})")

            print("\nMenu:")
            print("1. Tambah stok produk")
            print("2. Hapus produk")
            print("3. Kembali ke menu admin")

            pilih = input("Pilih menu: ").strip()
            
            # Menu tambah stok produk
            if pilih == "1":
                id_produk = input("Masukkan ID produk yang ingin diubah stoknya: ").strip()

                if not id_produk.isdigit():  # Validasi ID harus angka
                    print("ID produk tidak valid!")
                    pause()
                    continue

                # Cek apakah produk ada di database
                cur.execute("SELECT nama_produk, stok FROM produk WHERE id_produk=%s", (id_produk,))
                data = cur.fetchone()

                if not data:
                    print("Produk tidak ditemukan!")
                    pause()
                    continue

                print(f"\nProduk: {data[0]}")
                print(f"Stok saat ini: {data[1]}")
                
                # Input jumlah stok yang ingin ditambahkan
                stok_tambah = input("Masukkan jumlah stok yang ingin ditambahkan: ").strip()
                if not stok_tambah.isdigit():
                    print("Stok harus berupa angka!")
                    pause()
                    continue

                stok_baru = data[1] + int(stok_tambah)

                cur.execute("UPDATE produk SET stok=%s WHERE id_produk=%s", (stok_baru, id_produk))
                conn.commit()
                print(f"Stok berhasil ditambahkan! Stok sekarang: {stok_baru}")
                pause()
            
            # menu hapus produk
            elif pilih == "2":
                id_produk = input("Masukkan ID produk yang ingin dihapus: ").strip()
                if not id_produk.isdigit():
                    print("ID produk tidak valid!")
                    pause()
                    continue
            
                cur.execute("SELECT nama_produk FROM produk WHERE id_produk=%s", (id_produk,))
                cek = cur.fetchone()

                if not cek:
                    print("Produk tidak ditemukan!")
                    pause()
                    continue

                konfirmasi = input(f"Yakin ingin menghapus produk '{cek[0]}'? (y/n): ").lower().strip()
                if konfirmasi == 'y':

                    # Hapus produk dengan mengubah status is_deleted menjadi TRUE
                    cur.execute("UPDATE produk SET is_deleted = TRUE WHERE id_produk=%s", (id_produk,))
                    conn.commit()
                    print("Produk berhasil dihapus dari daftar!")
                else:
                    print("Penghapusan dibatalkan.")
                pause()

            elif pilih == "3":
                break
            else:
                print("Pilihan tidak valid!")
                pause()

    except Exception as e:
        print("Terjadi kesalahan:", e)
    finally:
        cur.close()
        conn.close()

# Fungsi untuk menampilkan daftar permintaan pesanan
def daftar_permintaan():
    conn, cur = connectDB()
    if not conn:
        pause()
        return

    try:
        while True:
            os.system('cls')
            print(r'''
            =============================================
                           DAFTAR PERMINTAAN           
            =============================================''')
            
            # Query untuk menampilkan pesanan yang masih berstatus 'diproses'
            cur.execute("""
                SELECT 
                    p.id_pesanan, 
                    u.nama_pengguna, 
                    p.status_pesanan,
                    p.tanggal_pesanan,
                    p.tanggal_pengiriman
                FROM pesanan p 
                JOIN pengguna u ON p.id_user = u.id_user
                WHERE p.status_pesanan = 'diproses'
                ORDER BY p.id_pesanan
            """)
            rows = cur.fetchall()
            # Jika tidak ada pesanan masuk
            if not rows:
                print("Tidak ada permintaan pesanan yang belum diproses.")
                pause()
                return
            
            # Menampilkan setiap pesanan
            for r in rows:
                print(f"\nID Pesanan     : {r[0]}")
                print(f"Pelanggan      : {r[1]}")
                print(f"Status Pesanan : {r[2]}")
                print(f"Tanggal Pesan  : {r[3]}")
                print(f"Tanggal Kirim  : {r[4]}")
                
                # Menampilkan rincian produk dari pesanan
                cur.execute("""
                    SELECT pr.nama_produk, rp.jumlah, rp.harga
                    FROM rincian_pesanan rp
                    JOIN produk pr ON pr.id_produk = rp.id_produk
                    WHERE rp.id_pesanan=%s
                """, (r[0],))
                detail = cur.fetchall()

                print("Isi Pesanan:")
                for d in detail:
                    print(f"   - {d[0]}  jumlah: {d[1]}  harga: Rp {d[2]}")

            print("\nMenu:")
            print("1. Terima / Tolak pesanan")
            print("2. Kembali")

            pilih = input("Pilih menu: ").strip()

            if pilih == "1":
                id_pesanan = input("Masukkan ID pesanan: ").strip()
                keputusan = input("Terima (y) / Tolak (n): ").lower().strip()
                
                # Ambil metode pembayaran dari pesanan
                cur.execute("""
                    SELECT m.jenis_metode_pembayaran
                    FROM pembayaran p
                    JOIN metode_pembayaran m ON p.id_metode_pembayaran = m.id_metode_pembayaran
                    WHERE p.id_pesanan=%s
                """, (id_pesanan,))
                bayar = cur.fetchone()

                if not bayar:
                    print("Data pembayaran tidak ditemukan!")
                    pause()
                    continue

                metode = bayar[0]

                if keputusan == 'y':
                    # Kurangi stok produk sesuai pesanan
                    cur.execute(""" 
                        SELECT id_produk, jumlah FROM rincian_pesanan
                        WHERE id_pesanan=%s
                    """, (id_pesanan,))
                    items = cur.fetchall()

                    for item in items:
                        cur.execute("""
                            UPDATE produk
                            SET stok = stok - %s
                            WHERE id_produk = %s
                        """, (item[1], item[0]))

                     # Ubah status pesanan menjadi diterima
                    cur.execute("""
                        UPDATE pesanan 
                        SET status_pesanan = 'diterima'
                        WHERE id_pesanan = %s
                    """, (id_pesanan,))
                    
                    # Update pembayaran sesuai metode
                    if metode.lower() == "transfer":
                        cur.execute("""
                            UPDATE pembayaran
                            SET status_pembayaran = 'lunas'
                            WHERE id_pesanan = %s
                        """, (id_pesanan,))
                        print("\nPesanan diterima (TRANSFER) → pembayaran: LUNAS")
                    else:
                        cur.execute("""
                            UPDATE pembayaran
                            SET status_pembayaran = 'COD (Bayar di lokasi)'
                            WHERE id_pesanan = %s
                        """, (id_pesanan,))
                        print("\nPesanan diterima (COD) → Pembayaran di lokasi")
            
                    conn.commit()
                    pause()
                    continue
                
                # Jika pesanan ditolak
                elif keputusan == 'n':
                    cur.execute("""
                        UPDATE pesanan 
                        SET status_pesanan = 'ditolak'
                        WHERE id_pesanan = %s
                    """, (id_pesanan,))

                    cur.execute("""
                        UPDATE pembayaran
                        SET status_pembayaran = 'dibatalkan'
                        WHERE id_pesanan = %s
                    """, (id_pesanan,))

                    conn.commit()
                    print("\nPesanan ditolak & pembayaran dibatalkan")
                    pause()
                    continue
            elif pilih == '2':
                break
            else:
                    print("Input tidak valid!")
                    pause()
                    continue
    finally:
        cur.close()
        conn.close()

# Fungsi untuk menampilkan dan memperbarui status pesanan
def status_pesanan():
    conn, cur = connectDB()
    if not conn:
        pause()
        return

    try:
        while True:
            os.system('cls')
            print(r'''
            =============================================
                            STATUS PESANAN            
            =============================================''')
           
            # Ambil semua data pesanan beserta statusnya
            cur.execute("SELECT id_pesanan, status_pesanan FROM pesanan ORDER BY id_pesanan")
            rows = cur.fetchall()
            
            # Tampilkan semua pesanan
            for r in rows:
                print(f"Pesanan {r[0]} | Status: {r[1]}")

            print("\nMenu:")
            print("1. Update status pesanan")
            print("2. Kembali")

            pilih = input("Pilih menu: ").strip()

            if pilih == "1":
                id_pesanan = input("Masukkan ID Pesanan: ").strip()
                print("\nPilih status baru:")
                print("1. diproses")
                print("2. dikirim")
                print("3. selesai")

                pilih2 = input("Masukkan pilihan status: ").strip()
                status_baru = None

                if pilih2 == '1':
                    status_baru = "diproses"
                elif pilih2 == '2':
                    status_baru = "dikirim"
                elif pilih2 == '3':
                    status_baru = "selesai"
                else:
                    print("Input tidak valid!")
                    pause()
                    continue
                
                # Update status di database
                cur.execute("""
                    UPDATE pesanan
                    SET status_pesanan = %s
                    WHERE id_pesanan = %s
                """, (status_baru, id_pesanan))
                conn.commit()

                print("\nStatus berhasil diperbarui!")
                pause()

            elif pilih == "2":
                break

            else:
                print("Pilihan tidak valid.")
                pause()

    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()

# Fungsi untuk menampilkan riwayat transaksi
def riwayat_transaksi():
    conn, cur = connectDB()
    if not conn:
        pause()
        return

    try:
        os.system('cls')
        print(r'''
        =============================================
                      RIWAYAT TRANSAKSI            
        =============================================''')
        
        # Ambil data transaksi pesanan beserta informasi pembayaran dan metode
        cur.execute("""
            SELECT 
                p.id_pembayaran, 
                COALESCE(m.jenis_metode_pembayaran, ' - ') AS metode,
                COALESCE(p.status_pembayaran, 'Belum Dibayar') AS status,
                ps.id_pesanan
            FROM pesanan ps
            LEFT JOIN pembayaran p ON ps.id_pesanan = p.id_pesanan
            LEFT JOIN metode_pembayaran m ON m.id_metode_pembayaran = p.id_metode_pembayaran
            ORDER BY ps.id_pesanan DESC
        """)
        
        rows = cur.fetchall()

        # Jika tidak ada data transaksi
        if not rows:
            print("Belum ada riwayat transaksi.")
        else:
            # Tampilkan semua data riwayat transaksi
            for r in rows:
                print(f"Pembayaran {r[0]} | Metode: {r[1]} | Status: {r[2]} | Pesanan: {r[3]}")

    except Exception as e:
        print("Gagal mengambil data transaksi!")
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()
    
    pause()

# Fungsi ini digunakan untuk menampilkan menu user
def menu_user(id_user):
    while True:
        os.system('cls')
        print(r'''
        =============================================
                       MENU PELANGGAN            
        =============================================''')
        print('1. Lihat Daftar Produk')
        print('2. Membeli Barang')
        print('3. Lihat Status Pesanan')
        print('4. Lihat Riwayat Transaksi')
        print('5. Logout')

        pilih = input("Pilih menu (1-5): ").strip()

        if pilih == '1':
            user_daftar_produk()
        elif pilih == '2':
            user_beli_barang(id_user)
        elif pilih == '3':
            user_status_pesanan(id_user)
        elif pilih == '4':
            user_riwayat_transaksi(id_user)
        elif pilih == '5':
            logout()
        else:
            print("Pilihan tidak valid.")
            pause()

# Fungsi ini digunakan untuk menampilkan daftar produk
def user_daftar_produk():
    conn, cur = connectDB()
    if not conn:
        pause()
        return

    try:
        os.system('cls')
        print(r'''
        =============================================
                        DAFTAR PRODUK            
        =============================================''')

        cur.execute("SELECT id_produk, nama_produk, harga, stok FROM produk WHERE is_deleted = FALSE ORDER BY id_produk")
        rows = cur.fetchall()

        # Tampilkan semua data produk
        for r in rows:
            print(f"{r[0]}. {r[1]} | Harga: Rp {r[2]} | Stok: {r[3]}")

    except Exception as e:
        print("Terjadi kesalahan:", e)
    finally:
        cur.close()
        conn.close()
    pause()

# Fungsi untuk melakukan pembelian produk
def user_beli_barang(id_user):
    conn, cur = connectDB()
    if not conn:
        pause()
        return

    try:
        os.system('cls')
        print(r'''
        =============================================
                        BELI PRODUK            
        =============================================''')
        cur.execute("SELECT id_produk, nama_produk, harga, stok FROM produk WHERE is_deleted = FALSE ORDER BY id_produk")
        rows = cur.fetchall()
        for r in rows:
            print(f"{r[0]}. {r[1]} | Harga: Rp {r[2]} | Stok: {r[3]}")
        
        # Input ID Produk dari user
        id_produk = input("Masukkan ID produk: ").strip()
        if not id_produk.isdigit():
            print("ID produk tidak valid!")
            pause()
            return
        id_produk = int(id_produk)
        
        # Input jumlah pembelian
        jumlah_str = input("Jumlah dibeli: ").strip()
        if not jumlah_str.isdigit():
            print("Jumlah tidak valid!")
            pause()
            return
        jumlah = int(jumlah_str)
        
        # Cek harga dan stok produk
        cur.execute("SELECT harga, stok FROM produk WHERE id_produk=%s", (id_produk,))
        produk = cur.fetchone()

        if not produk:
            print("Produk tidak ditemukan!")
            pause()
            return

        harga, stok = produk

        # Validasi stok cukup
        if jumlah > stok:
            print("Stok tidak cukup!")
            pause()
            return
        
        # Hitung total bayar
        total_harga = float(harga) * jumlah
        
         # Pilih desa untuk alamat pengiriman
        os.system('cls')
        print("=== PILIH KABUPATEN ===")
        cur.execute("SELECT id_kabupaten, nama_kabupaten FROM kabupaten ORDER BY id_kabupaten")
        for row in cur.fetchall():
            print(f"{row[0]}. {row[1]}")
        id_kabupaten = input("Pilih ID Kabupaten: ").strip()

        
        print("=== PILIH KECAMATAN ===")
        cur.execute("SELECT id_kecamatan, nama_kecamatan FROM kecamatan WHERE id_kabupaten=%s ORDER BY id_kecamatan", (id_kabupaten,))
        for row in cur.fetchall():
            print(f"{row[0]}. {row[1]}")
        id_kecamatan = input("Pilih ID Kecamatan: ").strip()


        print("=== PILIH DESA ===")
        cur.execute(
            "SELECT id_desa, nama_desa FROM desa WHERE id_kecamatan = %s ORDER BY id_desa",
            (id_kecamatan,)
            )
        desa_list = cur.fetchall()
        for d in desa_list:
            print(f"{d[0]}. {d[1]}")
        id_desa = input("Pilih ID Desa: ").strip()
        if not id_desa.isdigit():
            print("ID desa tidak valid!")
            pause()
            return
        id_desa = int(id_desa)

        # Input detail alamat dan tanggal kirim
        detail_alamat = input("Masukkan detail alamat lengkap (Nama jl, No): ").strip()
        tanggal_kirim = input("Tanggal pengiriman (YYYY-MM-DD): ").strip()
        
        # Simpan data pesanan dan ambil ID pesanan yang baru dibuat
        cur.execute("""
    INSERT INTO pesanan (
        tanggal_pesanan,
        tanggal_pengiriman,
        id_user,
        detail_alamat,
        id_kecamatan,
        id_desa,
        status_pesanan
    )
                    VALUES (CURRENT_DATE, %s, %s, %s, %s, %s, 'diproses')
                    RETURNING id_pesanan
                    """, (tanggal_kirim, id_user, detail_alamat, id_kecamatan, id_desa))
        id_pesanan = cur.fetchone()[0]

        
        # Simpan rincian pesanan (produk, jumlah, harga)
        cur.execute("""
            INSERT INTO rincian_pesanan (jumlah, harga, id_pesanan, id_produk)
            VALUES (%s, %s, %s, %s)
        """, (jumlah, harga, id_pesanan, id_produk))
        
        # Tampilkan total harga pesanan
        os.system('cls')
        print("Total harga yang harus dibayar: Rp", total_harga)

        # Pilih metode pembayaran
        print(r'''
        =============================================
                   PILIH METODE PEMBAYARAN            
        =============================================''')
        cur.execute("""
            SELECT id_metode_pembayaran, jenis_metode_pembayaran, nama_bank, no_rekening
            FROM metode_pembayaran
            ORDER BY id_metode_pembayaran
        """)
        metode_list = cur.fetchall()
        
        # Tampilkan metode pembayaran
        for m in metode_list:
            jenis_display = m[1] if m[1] else ''
            if jenis_display.lower() == "cod":
                print(f"{m[0]}. COD")
            else:
                bank_name = m[2] or '-'
                print(f"{m[0]}. Transfer via {bank_name}")
        
        # Input metode pembayaran
        id_metode = input("Pilih ID Metode Pembayaran: ").strip()
        if not id_metode.isdigit():
            print("Metode pembayaran tidak valid!")
            pause()
            return
        id_metode = int(id_metode)

        cur.execute("""
            SELECT jenis_metode_pembayaran, nama_bank, no_rekening
            FROM metode_pembayaran WHERE id_metode_pembayaran=%s
        """, (id_metode,))
        metode_data = cur.fetchone()

        if not metode_data:
            print("Metode pembayaran tidak ditemukan!")
            pause()
            return

        jenis, bank, norek = metode_data
        
        # Tentukan status pembayaran berdasarkan metode (transfer atau COD)
        status_pembayaran = None
        if jenis and jenis.lower().find("transfer") != -1:
            os.system('cls')
            print(r'''
            =============================================
                         TRANSFER REKENING           
            =============================================''')
            print(f"Bank               : {bank or '-'}")
            print(f"Nomor Rekening     : {norek or '-'}")
            print("Atas Nama          : PT SITRAGU MAKMUR")
            print("---------------------------------------------")
            print("Silakan lakukan pembayaran sebelum proses dikirim.")

            konfirmasi = input("\nSudah melakukan transfer? (y/n): ").lower().strip()
            if konfirmasi == "y":
                status_pembayaran = "menunggu verifikasi"
            else:
                status_pembayaran = "belum bayar"
        else:
            print("\nAnda memilih pembayaran COD.")
            status_pembayaran = "COD"
        
        # Simpan data pembayaran
        cur.execute("""
            INSERT INTO pembayaran (id_pesanan, id_metode_pembayaran, status_pembayaran)
            VALUES (%s, %s, %s)
            RETURNING id_pembayaran
        """, (id_pesanan, id_metode, status_pembayaran))
        id_pembayaran = cur.fetchone()[0]

        conn.commit()

        print("\nPesanan berhasil dibuat!")
        print("Status pembayaran:", status_pembayaran)

    except Exception as e:
        if conn:
            conn.rollback()
        print("Terjadi kesalahan saat proses pemesanan:", e)
    finally:
        if cur: cur.close()
        if conn: conn.close()

    pause()

# Fungsi untuk menampilkan status pesanan
def user_status_pesanan(id_user):
    conn, cur = connectDB()
    if not conn:
        pause()
        return

    try:
        os.system('cls')
        print(r'''
        =============================================
                     STATUS PESANAN ANDA            
        =============================================''')
        
        #ambil data status pesanan
        cur.execute("""
            SELECT id_pesanan, tanggal_pengiriman, status_pesanan
            FROM pesanan
            WHERE id_user=%s
            ORDER BY id_pesanan DESC
        """, (id_user,))

        rows = cur.fetchall()
        if not rows:
            print("Belum ada pesanan.")
        else:
            for r in rows:
                print(f"Pesanan {r[0]} | Pengiriman: {r[1]} | Status: {r[2]}")

    except Exception as e:
        print("Terjadi kesalahan:", e)
    finally:
        cur.close()
        conn.close()
    pause()

# fungsi untuk menampilkan riwayat transaksi pelanggan
def user_riwayat_transaksi(id_user):
    conn, cur = connectDB()
    if not conn:
        pause()
        return

    try:
        os.system('cls')
        print(r'''
        =========================================================
                           RIWAYAT TRANSAKSI ANDA          
        =========================================================''')

        cur.execute("""
            SELECT 
                py.id_pembayaran,
                ps.id_pesanan,
                TO_CHAR(ps.tanggal_pesanan, 'DD-MM-YYYY') AS tgl_pesan,
                
                STRING_AGG(pr.nama_produk, ', ') AS produk_dipesan,
                SUM(rp.jumlah) AS total_item,
                SUM(rp.jumlah * rp.harga) AS total_harga,
                
                ps.status_pesanan,
                COALESCE(py.status_pembayaran, 'Belum Dibayar') AS status_bayar,
                COALESCE(m.jenis_metode_pembayaran, '-') AS metode

            FROM pesanan ps
            JOIN rincian_pesanan rp ON ps.id_pesanan = rp.id_pesanan
            JOIN produk pr ON pr.id_produk = rp.id_produk
            LEFT JOIN pembayaran py ON ps.id_pesanan = py.id_pesanan
            LEFT JOIN metode_pembayaran m ON m.id_metode_pembayaran = py.id_metode_pembayaran
            WHERE ps.id_user = %s
            GROUP BY 
                py.id_pembayaran, ps.id_pesanan, ps.tanggal_pesanan, 
                ps.status_pesanan, py.status_pembayaran, 
                m.jenis_metode_pembayaran
            ORDER BY ps.id_pesanan DESC
        """, (id_user,))

        rows = cur.fetchall()

        if not rows:
            print("Belum ada riwayat transaksi.")
        else:
            print(f"{'ID Bayar':<10} {'ID Pesanan':<11} {'Produk':<25} {'Item':<6} {'Total (Rp)':<12} {'Pesanan':<10} {'Pembayaran':<14} {'Tgl Pesan':<12}")
            print("-" * 105)

            for r in rows:
                print(f"{r[0]:<10} {r[1]:<11} {r[3]:<25} {r[4]:<6} {r[5]:<12} {r[6]:<10} {r[7]:<14} {r[2]:<12}")

    except Exception as e:
        print("Terjadi kesalahan:", e)
    finally:
        cur.close()
        conn.close()
    pause()

if __name__== "__main__":
    menu_utama()  # Jalankan menu utama saat file dieksekusi langsung