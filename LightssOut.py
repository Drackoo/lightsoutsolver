import tkinter as tk
from tkinter import scrolledtext, Toplevel, Canvas
import random
import time
from collections import deque

class PermainanLightsOut:
    def __init__(self, root):
        self.root = root
        self.root.title("Permainan Lights Out")
        self.ukuran = 3
        self.tombol = [[None for _ in range(self.ukuran)] for _ in range(self.ukuran)]
        self.langkah = []
        
        self.pohon_window = None
        self.canvas_pohon = None

        for baris in range(self.ukuran):
            for kolom in range(self.ukuran):
                tombol = tk.Button(self.root, width=10, height=5, command=lambda r=baris, c=kolom: self.ubah_lampu(r, c))
                tombol.grid(row=baris, column=kolom, padx=0, pady=0)
                self.tombol[baris][kolom] = tombol

        self.langkah_tampilan = scrolledtext.ScrolledText(self.root, width=40, height=10)
        self.langkah_tampilan.grid(row=self.ukuran, column=0, columnspan=self.ukuran)

        tombol_selesaikan = tk.Button(self.root, text="Selesaikan (Brute Force)", command=self.selesaikan_dan_tampilkan_brute_force)
        tombol_selesaikan.grid(row=self.ukuran + 1, column=0, columnspan=self.ukuran)

        tombol_selesaikan = tk.Button(self.root, text="Selesaikan (Backtracking)", command=self.selesaikan_dan_tampilkan_backtrack)
        tombol_selesaikan.grid(row=self.ukuran + 2, column=0, columnspan=self.ukuran)

        self.acak_grid()
        self.perbarui_tampilan_langkah()

    def ubah_lampu(self, baris, kolom):
        self.langkah.append((baris, kolom))
        self.perbarui_tampilan_langkah()

        self.ubah_tombol(baris, kolom)
        if baris > 0:
            self.ubah_tombol(baris-1, kolom)
        if baris < self.ukuran - 1:
            self.ubah_tombol(baris+1, kolom)
        if kolom > 0:
            self.ubah_tombol(baris, kolom-1)
        if kolom < self.ukuran - 1:
            self.ubah_tombol(baris, kolom+1)
        
        if self.periksa_kemenangan():
            self.tampilkan_pesan_kemenangan()
            return True

        return False

    def ubah_tombol(self, baris, kolom):
        tombol = self.tombol[baris][kolom]
        if tombol["bg"] == "SystemButtonFace":
            tombol.config(bg="yellow")
        else:
            tombol.config(bg="SystemButtonFace")

    def periksa_kemenangan(self):
        for baris in range(self.ukuran):
            for kolom in range(self.ukuran):
                if self.tombol[baris][kolom]["bg"] == "yellow":
                    return False
        return True

    def tampilkan_pesan_kemenangan(self):
        pesan_kemenangan = tk.Label(self.root, text="Anda Menang!", font=("Arial", 24))
        pesan_kemenangan.grid(row=self.ukuran + 3, column=0, columnspan=self.ukuran)

    def perbarui_tampilan_langkah(self):
        langkah_teks = "Langkah yang diambil:\n" + "\n".join([f"Langkah {i+1}: Tombol ({r},{c})" for i, (r, c) in enumerate(self.langkah)])
        self.langkah_tampilan.delete("1.0", tk.END)
        self.langkah_tampilan.insert(tk.END, langkah_teks)

    def acak_grid(self):
        for _ in range(random.randint(5, 15)):
            baris = random.randint(0, self.ukuran - 1)
            kolom = random.randint(0, self.ukuran - 1)
            self.ubah_tombol(baris, kolom)

    def selesaikan_brute_force(self):
        keadaan_awal = [[tombol["bg"] for tombol in baris] for baris in self.tombol]
        langkah_awal = []
        antrian = deque([(keadaan_awal, langkah_awal)])
        keadaan_dikunjungi = set()

        if self.periksa_keadaan_kemenangan(keadaan_awal):
            return langkah_awal

        while antrian:
            keadaan_sekarang, langkah_sekarang = antrian.popleft()
            keadaan_tuple = tuple(tuple(baris) for baris in keadaan_sekarang)

            if keadaan_tuple not in keadaan_dikunjungi:
                keadaan_dikunjungi.add(keadaan_tuple)

                if self.periksa_keadaan_kemenangan(keadaan_sekarang):
                    return langkah_sekarang

                for baris in range(self.ukuran):
                    for kolom in range(self.ukuran):
                        keadaan_baru = self.ubah_keadaan_lampu(keadaan_sekarang, baris, kolom)
                        langkah_baru = langkah_sekarang + [(baris, kolom)]
                        antrian.append((keadaan_baru, langkah_baru))

        return None

    def ubah_keadaan_lampu(self, keadaan, baris, kolom):
        keadaan_baru = [list(baris) for baris in keadaan]
        self.ubah_tombol_keadaan(keadaan_baru, baris, kolom)
        if baris > 0:
            self.ubah_tombol_keadaan(keadaan_baru, baris-1, kolom)
        if baris < self.ukuran - 1:
            self.ubah_tombol_keadaan(keadaan_baru, baris+1, kolom)
        if kolom > 0:
            self.ubah_tombol_keadaan(keadaan_baru, baris, kolom-1)
        if kolom < self.ukuran - 1:
            self.ubah_tombol_keadaan(keadaan_baru, baris, kolom+1)
        return keadaan_baru

    def ubah_tombol_keadaan(self, keadaan, baris, kolom):
        if keadaan[baris][kolom] == "SystemButtonFace":
            keadaan[baris][kolom] = "yellow"
        else:
            keadaan[baris][kolom] = "SystemButtonFace"

    def periksa_keadaan_kemenangan(self, keadaan):
        for baris in range(self.ukuran):
            for kolom in range(self.ukuran):
                if keadaan[baris][kolom] == "yellow":
                    return False
        return True

    def selesaikan_dan_tampilkan_brute_force(self):
        waktu_mulai = time.time()
        solusi = self.selesaikan_brute_force()
        waktu_selesai = time.time()

        if solusi:
            langkah_teks = "\n".join([f"Langkah {i+1}: Tombol ({r},{c})" for i, (r, c) in enumerate(solusi)])
            self.langkah_tampilan.insert(tk.END, "\n\nLangkah-langkah (Brute Force):\n" + langkah_teks)
        else:
            self.langkah_tampilan.insert(tk.END, "\n\nTidak ditemukan solusi.")

        waktu_eksekusi = waktu_selesai - waktu_mulai
        self.langkah_tampilan.insert(tk.END, f"\n\nWaktu Eksekusi (Brute Force): {waktu_eksekusi:.4f} detik")

    def selesaikan_backtrack(self, kedalaman_maks=5):
        keadaan_awal = [[tombol["bg"] for tombol in baris] for baris in self.tombol]
        langkah_awal = []
        keadaan_dikunjungi = set()
        solusi = self.backtrack(keadaan_awal, langkah_awal, kedalaman_maks, keadaan_dikunjungi)
        return solusi

    def backtrack(self, keadaan, langkah, kedalaman_maks, keadaan_dikunjungi):
        tumpukan = [(keadaan, langkah, kedalaman_maks)]
        if self.pohon_window:
            self.gambar_pohon_tumpukan(tumpukan)

        while tumpukan:
            keadaan_sekarang, langkah_sekarang, kedalaman_sekarang = tumpukan.pop()

            if self.periksa_keadaan_kemenangan(keadaan_sekarang):
                return langkah_sekarang

            if kedalaman_sekarang == 0:
                continue

            keadaan_tuple = tuple(tuple(baris) for baris in keadaan_sekarang)
            if keadaan_tuple in keadaan_dikunjungi:
                continue

            keadaan_dikunjungi.add(keadaan_tuple)

            for baris in range(self.ukuran):
                for kolom in range(self.ukuran):
                    keadaan_baru = self.ubah_keadaan_lampu(keadaan_sekarang, baris, kolom)
                    langkah_baru = langkah_sekarang + [(baris, kolom)]
                    tumpukan.append((keadaan_baru, langkah_baru, kedalaman_sekarang - 1))

            if self.pohon_window:
                self.gambar_pohon_tumpukan(tumpukan)

        return None

    def selesaikan_dan_tampilkan_backtrack(self):
        kedalaman_awal = 5
        kedalaman_maks = kedalaman_awal

        self.langkah_tampilan.insert(tk.END, f"\n\nMencoba dengan Kedalaman Maksimal: {kedalaman_maks}\n")

        self.buat_jendela_pohon()

        while True:
            waktu_mulai = time.time()
            solusi = self.selesaikan_backtrack(kedalaman_maks)
            waktu_selesai = time.time()
            
            if solusi:
                langkah_teks = "\n".join([f"Langkah {i+1}: Tombol ({r},{c})" for i, (r, c) in enumerate(solusi)])
                self.langkah_tampilan.insert(tk.END, "\nLangkah-langkah Backtracking):\n" + langkah_teks)
                break
            else:
                kedalaman_maks += 5
                self.langkah_tampilan.insert(tk.END, f"\nKedalaman maksimum ditingkatkan menjadi: {kedalaman_maks}\n")

        waktu_eksekusi = waktu_selesai - waktu_mulai
        self.langkah_tampilan.insert(tk.END, f"\n\nWaktu Eksekusi (Backtracking): {waktu_eksekusi:.4f} detik")

    def buat_jendela_pohon(self):
        if self.pohon_window is not None and tk.Toplevel.winfo_exists(self.pohon_window):
            return

        self.pohon_window = Toplevel(self.root)
        self.pohon_window.title("Visualisasi Pohon Proses")
        self.canvas_pohon = Canvas(self.pohon_window, width=800, height=1200)
        self.canvas_pohon.pack()

    def gambar_pohon_tumpukan(self, tumpukan):
        if not self.canvas_pohon:
            return

        self.canvas_pohon.delete("all")
        node_map = {}
        level_map = {}
        node_id = 0

        for i, (keadaan, langkah, kedalaman) in enumerate(tumpukan):
            level = len(langkah)
            x = 50 + (level * 150)
            y = 50 + (level_map.get(level, 0) * 150)
            warna = "blue" if langkah else "red"

            self.canvas_pohon.create_oval(x-20, y-20, x+20, y+20, fill=warna)
            self.canvas_pohon.create_text(x, y, text=str(len(langkah)))

            node_map[node_id] = (x, y)
            matriks_teks = "\n".join([" ".join(["X" if cell == "yellow" else "O" for cell in baris]) for baris in keadaan])
            self.canvas_pohon.create_text(x, y + 30, text=matriks_teks, font=("Arial", 8))

            if langkah:
                parent_id = node_id - 1
                if parent_id in node_map:
                    x1, y1 = node_map[parent_id]
                    x2, y2 = node_map[node_id]
                    self.canvas_pohon.create_line(x1, y1, x2, y2)

            node_id += 1
            level_map[level] = level_map.get(level, 0) + 1

# Membuat jendela utama
root = tk.Tk()

# Inisialisasi permainan
permainan = PermainanLightsOut(root)

# Memulai loop peristiwa Tkinter
root.mainloop()
