import os
import sys
import psycopg2

def connectDB():
    try:
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="0402",
            dbname="SITRAGUOKE"
        )
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print("Gagal koneksi ke database:", e)
        return None, None

def pause():

    input("\nTekan ENTER untuk melanjutkan...")


def logout():
    print("\nTerima kasih telah menggunakan SITRAGU. Sampai jumpa!")
    pause()
    sys.exit(0)

def menu_utama():
    while True:
        os.system('cls')
        print(r'''
        =============================================
                 SELAMAT DATANG DI SITRAGU!            
        =============================================''')
        print("1. Registrasi")
        print("2. Login")
        print("3. Log out")

        pilih = input("Masukkan pilihan (1-3): ").strip()
        if pilih == '1':
            registrasi()
        elif pilih == '2':
            login()
        elif pilih == '3':
            logout()
        else:
            print("Pilihan tidak valid.")
            pause()

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

        nama = input("Nama : ").strip().title()
        email = input("Email : ").strip().lower()
        password = input("Password : ").strip()

        while True:
            no_telepon = input("No telepon : ").strip()
            if no_telepon.isdigit():
                break
            print("No telepon hanya boleh angka!")

        cur.execute("SELECT email FROM pengguna WHERE email=%s", (email,))
        if cur.fetchone():
            print("\nEmail sudah digunakan!")
            pause()
            return

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

        if user[1] == 'admin':
            print("\nLogin berhasil. Selamat datang admin!")
            pause()
            menu_admin()
        else:
            print("\nLogin berhasil sebagai pelanggan!")
            pause()
            menu_user(user[0])

    except Exception as e:
        print("Login gagal!", e)
    finally:
        cur.close()
        conn.close()

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

        tambah = input("\nMasukkan jumlah bahan baku baru yang ingin ditambahkan: ").strip()
        if not tambah.isdigit():
            print("Input harus berupa angka!")
            pause()
            return
        tambah = int(tambah)

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
            cur.execute("SELECT id_produk, nama_produk, harga, stok FROM produk WHERE is_deleted = FALSE ORDER BY id_produk ASC")
            produk = cur.fetchall()

            for p in produk:
                print(f"{p[0]}. {p[1]} - Rp {p[2]} (Stok: {p[3]})")

            print("\nMenu:")
            print("1. Tambah stok produk")
            print("2. Hapus produk")
            print("3. Kembali ke menu admin")

            pilih = input("Pilih menu: ").strip()

            if pilih == "1":
                id_produk = input("Masukkan ID produk yang ingin diubah stoknya: ").strip()

                if not id_produk.isdigit():
                    print("ID produk tidak valid!")
                    pause()
                    continue

                cur.execute("SELECT nama_produk, stok FROM produk WHERE id_produk=%s", (id_produk,))
                data = cur.fetchone()

                if not data:
                    print("Produk tidak ditemukan!")
                    pause()
                    continue

                print(f"\nProduk: {data[0]}")
                print(f"Stok saat ini: {data[1]}")

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

            if not rows:
                print("Tidak ada permintaan pesanan yang belum diproses.")
                pause()
                return

            for r in rows:
                print(f"\nID Pesanan     : {r[0]}")
                print(f"Pelanggan      : {r[1]}")
                print(f"Status Pesanan : {r[2]}")
                print(f"Tanggal Pesan  : {r[3]}")
                print(f"Tanggal Kirim  : {r[4]}")

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

                    cur.execute("""
                        UPDATE pesanan 
                        SET status_pesanan = 'diterima'
                        WHERE id_pesanan = %s
                    """, (id_pesanan,))

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

                else:
                    print("Input tidak valid!")
                    pause()
                    continue
    finally:
        cur.close()
        conn.close()

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

            cur.execute("SELECT id_pesanan, status_pesanan FROM pesanan ORDER BY id_pesanan")
            rows = cur.fetchall()

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

        if not rows:
            print("Belum ada riwayat transaksi.")
        else:
            for r in rows:
                print(f"Pembayaran {r[0]} | Metode: {r[1]} | Status: {r[2]} | Pesanan: {r[3]}")

    except Exception as e:
        print("Gagal mengambil data transaksi!")
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()
    
    pause()

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

        for r in rows:
            print(f"{r[0]}. {r[1]} | Harga: Rp {r[2]} | Stok: {r[3]}")

    except Exception as e:
        print("Terjadi kesalahan:", e)
    finally:
        cur.close()
        conn.close()
    pause()

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

        id_produk = input("Masukkan ID produk: ").strip()
        if not id_produk.isdigit():
            print("ID produk tidak valid!")
            pause()
            return
        id_produk = int(id_produk)

        jumlah_str = input("Jumlah dibeli: ").strip()
        if not jumlah_str.isdigit():
            print("Jumlah tidak valid!")
            pause()
            return
        jumlah = int(jumlah_str)

        cur.execute("SELECT harga, stok FROM produk WHERE id_produk=%s", (id_produk,))
        produk = cur.fetchone()

        if not produk:
            print("Produk tidak ditemukan!")
            pause()
            return

        harga, stok = produk
        if jumlah > stok:
            print("Stok tidak cukup!")
            pause()
            return

        total_harga = float(harga) * jumlah

        os.system('cls')
        print("=== PILIH DESA ===")

        cur.execute("SELECT id_desa, nama_desa FROM desa ORDER BY id_desa")
        desa_list = cur.fetchall()

        for d in desa_list:
            print(f"{d[0]}. {d[1]}")

        id_desa = input("Pilih ID Desa: ").strip()
        if not id_desa.isdigit():
            print("ID desa tidak valid!")
            pause()
            return
        id_desa = int(id_desa)

        detail_alamat = input("Masukkan detail alamat lengkap: ").strip()
        tanggal_kirim = input("Tanggal pengiriman (YYYY-MM-DD): ").strip()

        cur.execute("""
            INSERT INTO pesanan (
                tanggal_pesanan,
                tanggal_pengiriman,
                id_user,
                detail_alamat,
                id_desa,
                status_pesanan
            ) VALUES (CURRENT_DATE, %s, %s, %s, %s, 'diproses')
            RETURNING id_pesanan
        """, (tanggal_kirim, id_user, detail_alamat, id_desa))
        id_pesanan = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO rincian_pesanan (jumlah, harga, id_pesanan, id_produk)
            VALUES (%s, %s, %s, %s)
        """, (jumlah, harga, id_pesanan, id_produk))

        os.system('cls')
        print("Total harga yang harus dibayar: Rp", total_harga)

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

        for m in metode_list:
            jenis_display = m[1] if m[1] else ''
            if jenis_display.lower() == "cod":
                print(f"{m[0]}. COD")
            else:
                bank_name = m[2] or '-'
                print(f"{m[0]}. Transfer via {bank_name}")

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

def user_riwayat_transaksi(id_user):
    conn, cur = connectDB()
    if not conn:
        pause()
        return

    try:
        os.system('cls')
        print(r'''
        =============================================
                   RIWAYAT TRANSAKSI ANDA            
        =============================================''')

        cur.execute("""
            SELECT 
                p.id_pembayaran, 
                COALESCE(m.jenis_metode_pembayaran, ' - ') AS metode, 
                COALESCE(p.status_pembayaran, 'Belum Dibayar') AS status, 
                ps.id_pesanan
            FROM pesanan ps
            LEFT JOIN pembayaran p ON ps.id_pesanan = p.id_pesanan
            LEFT JOIN metode_pembayaran m ON m.id_metode_pembayaran = p.id_metode_pembayaran
            WHERE ps.id_user=%s
            ORDER BY ps.id_pesanan DESC
        """, (id_user,))

        rows = cur.fetchall()
        if not rows:
            print("Belum ada riwayat transaksi.")
        else:
            for r in rows:
                print(f"Pembayaran {r[0]} | Pesanan {r[3]} | Metode: {r[1]} | Status: {r[2]}")

    except Exception as e:
        print("Terjadi kesalahan:", e)
    finally:
        cur.close()
        conn.close()
    pause()

if __name__ == "__main__":
    menu_utama()